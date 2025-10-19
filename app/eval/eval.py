# ================================================================
# RAG Evaluation Script (RAGAS + Ollama + Qdrant)
# ================================================================

import os
import torch
import json
from pathlib import Path
from dotenv import load_dotenv

# === Local imports ===
from app.llm.chat import ask_rag
from app.vector_rag.collections import COLLECTIONS
from app.vector_rag.indexer import load_and_index_data

# === RAGAS imports ===
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)

# === LangChain + Ollama ===
from langchain_ollama import OllamaLLM
from langchain.schema import LLMResult

# ================================================================
# Setup & Configuration
# ================================================================

load_dotenv()

# Manually set OpenAI key (required by some RAGAS components)
os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("CHAT_MODEL", "gemma3:1b")
TOP_K = 3
THRESHOLD = 0.1

# ================================================================
# Safe Ollama Wrapper (ensure valid JSON outputs)
# ================================================================

class SafeOllamaWrapper(OllamaLLM):
    """Force LLM outputs into valid JSON strings for RAGAS evaluation."""

    def generate(self, prompts, stop=None):
        raw = super().generate(prompts, stop)
        for gen in raw.generations:
            for g in gen:
                text = g.text.strip()
                if not text.startswith("{"):
                    g.text = '{"result": "' + text.replace('"', '\\"') + '"}'
        return raw


# ================================================================
# RAG Pipeline: Retrieval + Generation
# ================================================================

def answer_and_contexts(query: str):
    """
    Retrieve top-K relevant documents from Qdrant and generate an answer.
    Returns:
        answer (str): model-generated answer
        contexts (List[str]): list of retrieved document contents
    """
    store = COLLECTIONS["books"]
    # load_and_index_data(store, "")
    results = store.search(query=query, top_k=TOP_K, threshold=THRESHOLD)

    contexts = [
        p.payload.get("content", "")
        for p in results
        if p.payload and p.payload.get("content")
    ] if results else []

    answer = ask_rag(query, contexts if contexts else [""])
    return answer, contexts

# ================================================================
# Load test set (from gen_testset.py output)
# ================================================================

dir_path = Path(os.path.dirname(__file__))
testset_path = dir_path / "test_set.json"

print(f"📂 Loading test set from: {testset_path}")

with open(testset_path, "r", encoding="utf-8") as f:
    test_data = json.load(f)

# Flatten all questions and answers
sample_queries = []
expected_responses = []

for item in test_data:
    for qa in item.get("qas", []):
        sample_queries.append(qa.get("question", ""))
        expected_responses.append(qa.get("answer", ""))

print(f"✅ Loaded {len(sample_queries)} QA pairs for evaluation.")



# ================================================================
# Build Evaluation Dataset
# ================================================================

dataset = []
for query, reference in zip(sample_queries, expected_responses):
    answer, contexts = answer_and_contexts(query)
    dataset.append({
        "user_input": query,
        "retrieved_contexts": contexts,
        "response": answer,
        "reference": reference,
    })

evaluation_dataset = EvaluationDataset.from_list(dataset)

# Try to clear GPU cache (if any)
try:
    torch.cuda.empty_cache()
except Exception:
    pass


# ================================================================
# Setup LLM Evaluator
# ================================================================

# eval_llm = SafeOllamaWrapper(model=MODEL_NAME, temperature=0)
# evaluator_llm = LangchainLLMWrapper(eval_llm)

from langchain_openai import ChatOpenAI
from ragas.llms import LangchainLLMWrapper

# GPT-4o-mini model (OpenAI)
eval_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=1024,
)

# Wrap for RAGAS compatibility
evaluator_llm = LangchainLLMWrapper(eval_llm)



# ================================================================
# Safe Evaluation Wrapper (handles RAGAS version changes)
# ================================================================

def evaluate_safe(dataset, metrics, llm):
    """Safely run RAGAS evaluation for multiple RAGAS versions."""
    try:
        return evaluate(dataset=dataset, metrics=metrics, llm=llm, batch_size=1)
    except TypeError:
        return evaluate(dataset=dataset, metrics=metrics, llm=llm)


# ================================================================
# Run Evaluation
# ================================================================

if __name__ == "__main__":
    print("🚀 Starting RAG Evaluation...\n")

    metrics = [
        Faithfulness(),
        AnswerRelevancy(),
        ContextPrecision(),
        ContextRecall(),
    ]

    results = evaluate_safe(
        dataset=evaluation_dataset,
        metrics=metrics,
        llm=evaluator_llm,
    )

    print("\n=== ✅ RAGAS RESULTS ===")
    print(results)

    try:
        print(results.to_pandas())
    except Exception:
        pass
