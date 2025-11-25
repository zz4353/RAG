import os
import json
from pathlib import Path
from dotenv import load_dotenv

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_recall,
    context_precision,
)

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# --- Imports from your original project ---
from app.llm.chat import ask_rag
from app.vector_rag.collections import COLLECTIONS
from app.graph_rag.retriever import search_graph
from app.graph_rag.collections import graph

# Tải các biến môi trường
load_dotenv()

# --- 1. Cấu hình ---
CRITIC_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"
TOP_K = 3
THRESHOLD = 0.1

# Đường dẫn đến file test_set.json
dir_path = Path(__file__).parent
testset_path = dir_path / "test_set.json"

# --- 2. Các hàm RAG tùy chỉnh của bạn ---
def answer_and_contexts_rag_only(question: str):
    store = COLLECTIONS["phones"]
    results = store.search(query=question, top_k=TOP_K, threshold=THRESHOLD)

    contexts = [
        p.get("content", "")
        for p in results
        if p and p.get("content")
    ] if results else []

    answer = ask_rag(question, contexts if contexts else [""])
    return answer, contexts


def answer_and_contexts_hybrid(question: str):
    store = COLLECTIONS["phones"]
    vector_rag_results = store.search(query=question, top_k=TOP_K, threshold=THRESHOLD)
    graph_rag_results = search_graph(graph, question)
    
    vector_contexts = [
        p.get("content", "")
        for p in vector_rag_results
        if p and p.get("content")
    ] if vector_rag_results else []
    
    graph_contexts = graph_rag_results if graph_rag_results else []
    
    contexts = vector_contexts + graph_contexts
    
    answer = ask_rag(question, contexts if contexts else [""])
    return answer, contexts


# --- 3. Hàm xây dựng dataset từ test_set.json ---
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
    print(f"Processing {len(sample_queries)} questions for {option}...")
    for idx, (question, reference) in enumerate(zip(sample_queries, expected_responses)):
        print(f"  [{idx+1}/{len(sample_queries)}] Processing: {question[:50]}...")
        
        if option == "rag_only":
            answer, contexts = answer_and_contexts_rag_only(question)
        elif option == "hybrid":
            answer, contexts = answer_and_contexts_hybrid(question)
        
        dataset.append({
            "question": question,
            "contexts": contexts,
            "answer": answer,
            "ground_truth": reference,
        })
    
    # Chuyển đổi sang Dataset của Hugging Face
    eval_dataset = Dataset.from_list(dataset)
    return eval_dataset


# --- 4. Hàm đánh giá an toàn ---
def evaluate_safe(dataset, metrics, llm, embeddings):
    try:
        return evaluate(
            dataset=dataset, 
            metrics=metrics, 
            llm=llm, 
            embeddings=embeddings,
            batch_size=4
        )
    except TypeError:
        return evaluate(
            dataset=dataset, 
            metrics=metrics, 
            llm=llm, 
            embeddings=embeddings
        )


# --- 5. Chạy đánh giá ---
if __name__ == "__main__":
    # Kiểm tra xem file test_set.json có tồn tại không
    if not testset_path.exists():
        print(f"Error: {testset_path} not found!")
        exit()
    
    print(f"Test set file found: {testset_path}")
    
    # Khởi tạo LLM và embeddings cho đánh giá
    critic_llm = ChatOpenAI(model=CRITIC_MODEL, temperature=0)
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    
    # Định nghĩa các metrics
    metrics = [
        context_precision,
        context_recall,
        faithfulness,
        answer_relevancy,
    ]
    
    # Chạy đánh giá cho từng phương pháp RAG
    for option in ["rag_only", "hybrid"]:
        print(f"\n{'='*80}")
        print(f"Running evaluation for: {option.upper()}")
        print(f"{'='*80}\n")
        
        # Xây dựng dataset từ test_set.json
        eval_dataset = data_constructor(testset_path, option)
        
        # Chạy đánh giá
        print(f"Evaluating {len(eval_dataset)} samples...")
        result = evaluate_safe(eval_dataset, metrics, critic_llm, embeddings)
        
        # Chuyển kết quả sang DataFrame
        df = result.to_pandas()
        
        # In kết quả
        print(f"\nResults for {option}:")
        print(df)
        print(f"\nSummary statistics for {option}:")
        print(df.describe())
        
        # Lưu kết quả ra file CSV
        csv_filename = f"ragas_results_{option}.csv"
        df.to_csv(csv_filename, index=False, encoding="utf-8")
        print(f"\nResults saved to {csv_filename}")
        
        # --- Lưu log ra file text ---
        log_filename = f"ragas_results_{option}.log"
        with open(log_filename, "w", encoding="utf-8") as f:
            f.write(f"Results for {option}:\n")
            f.write(df.to_string(index=False))
            f.write("\n\nSummary statistics:\n")
            f.write(df.describe().to_string())
        print(f"Log saved to {log_filename}")
    
    print(f"\n{'='*80}")
    print("All evaluations finished.")
    print(f"{'='*80}")