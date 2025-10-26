import os
import torch
import json
from pathlib import Path
from dotenv import load_dotenv

from app.llm.chat import ask_rag
from app.vector_rag.collections import COLLECTIONS
from app.vector_rag.indexer import load_and_index_data

from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)

load_dotenv()

os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("CHAT_MODEL", "gemma3:1b")
TOP_K = 3
THRESHOLD = 0.1

def answer_and_contexts_rag_only(question: str):
    store = COLLECTIONS["phones"]
    # load_and_index_data(store, "")
    results = store.search(query=question, top_k=TOP_K, threshold=THRESHOLD)

    contexts = [
        p.get("content", "")
        for p in results
        if p and p.get("content")
    ] if results else []

    answer = ask_rag(question, contexts if contexts else [""])
    return answer, contexts


def answer_and_contexts_hybrid(question: str):
    from app.graph_rag.retriever import search_graph
    from app.graph_rag.collections import graph
    store = COLLECTIONS["phones"]
    vector_rag_results = store.search(query=question, top_k=TOP_K, threshold=THRESHOLD)
    graph_rag_results = search_graph(graph, question)
    
    # Extract contexts from vector results (dictionaries with content)
    vector_contexts = [
        p.get("content", "")
        for p in vector_rag_results
        if p and p.get("content")
    ] if vector_rag_results else []
    
    # Graph results are already strings (sentences)
    graph_contexts = graph_rag_results if graph_rag_results else []
    
    # Combine all contexts
    contexts = vector_contexts + graph_contexts
    
    answer = ask_rag(question, contexts if contexts else [""])
    return answer, contexts


dir_path = Path(os.path.dirname(__file__))
testset_path = dir_path / "test_set.json"


def evaluate_safe(dataset, metrics, llm):
    """Safely run RAGAS evaluation for multiple RAGAS versions."""
    try:
        return evaluate(dataset=dataset, metrics=metrics, llm=llm, batch_size=1)
    except TypeError:
        return evaluate(dataset=dataset, metrics=metrics, llm=llm)
   
   
def data_constructor(testset_path, option):
    with open(testset_path, "r", encoding="utf-8") as f:
        test_data = json.load(f)
         
    # Flatten all questions and answers
    sample_queries = []
    expected_responses = []
    
    for item in test_data:
        for qa in item.get("qas", []):
            sample_queries.append(qa.get("question", ""))
            expected_responses.append(qa.get("answer", ""))
      
    dataset = []      
    for question, reference in zip(sample_queries, expected_responses):
        if option == "rag_only":
            answer, contexts = answer_and_contexts_rag_only(question)
        if option == "hybrid":
            answer, contexts = answer_and_contexts_hybrid(question)
        dataset.append({
            "user_input": question,
            "retrieved_contexts": contexts,
            "response": answer,
            "reference": reference,
        })

    evaluation_dataset = EvaluationDataset.from_list(dataset)
    return evaluation_dataset


if __name__ == "__main__":
    print("Starting RAG Evaluation...\n")

    metrics = [
        Faithfulness(),
        AnswerRelevancy(),
        ContextPrecision(),
        ContextRecall(),
    ]
    
    # Try to clear GPU cache (if any)
    try:
        torch.cuda.empty_cache()
    except Exception:
        pass
    
    
    from langchain_openai import ChatOpenAI
    from ragas.llms import LangchainLLMWrapper
    eval_llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        max_tokens=1024,
    )

# Wrap for RAGAS compatibility
evaluator_llm = LangchainLLMWrapper(eval_llm)
for option in ["hybrid", "rag_only"]:
    results = evaluate_safe(
        dataset=data_constructor(testset_path, option),
        metrics=metrics,
        llm=evaluator_llm,
    )

    print("\n RAGAS RESULTS")
    print(results)

    # --- Save results to log file ---
    log_file = f"ragas_results_{option}.txt"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\n==============================\n")
        f.write(f"RAGAS RESULTS for option: {str(option)}\n")
        f.write(str(results))
        f.write("\n")

        # Nếu có thể chuyển sang pandas, lưu thêm bảng chi tiết
        try:
            df = results.to_pandas()
            f.write("\nPandas Results:\n")
            f.write(df.to_string())
        except Exception:
            f.write("\n(Pandas conversion failed)\n")

    try:
        print(results.to_pandas())
    except Exception:
        pass
