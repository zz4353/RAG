# RAG/app/eval/eval.py
# python3 -m eval.eval.py
import os
# os.environ.setdefault("GIT_PYTHON_REFRESH", "quiet")  # tránh GitPython đòi git binary

import torch
from dotenv import load_dotenv

# Import from local modules
from app.llm.chat import ask_rag
from app.vector_rag.collections import COLLECTIONS

# Ragas
from ragas import EvaluationDataset, evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import Faithfulness, AnswerRelevancy, ContextPrecision, ContextRecall

# LangChain Ollama
from langchain_ollama import OllamaLLM

load_dotenv()

# Boc LLM ep dinh dang dau ra Json
from langchain.schema import LLMResult

class SafeOllamaWrapper(OllamaLLM):
    def generate(self, prompts, stop=None):
        # Ép output về JSON hợp lệ
        raw = super().generate(prompts, stop)
        for gen in raw.generations:
            for g in gen:
                if not g.text.strip().startswith("{"):
                    g.text = '{"result": "' + g.text.strip().replace('"', '\\"') + '"}'
        return raw




# ====== Cấu hình ======
os.environ["OPENAI_API_KEY"] = "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"
MODEL_NAME = os.getenv("CHAT_MODEL", "gemma3:1b")
TOP_K = 3
THRESHOLD = 0.1

# import test set
from app.eval.test_set import sample_queries, expected_responses


# ====== Hàm lấy câu trả lời + ngữ cảnh theo RAG ======
def answer_and_contexts(q: str):
    # 1) Retrieve từ Qdrant
    store = COLLECTIONS["books"]
    results = store.search(query=q, top_k=TOP_K, threshold=THRESHOLD)

    # Nếu không có kết quả, để trống context để đánh giá độ phù hợp
    if not results:
        docs = []
    else:
        docs = [p.payload.get("content", "") for p in results if p.payload and p.payload.get("content")]

    # 2) Gọi RAG để tạo câu trả lời (nếu không có docs, ask_rag sẽ trả lời theo template)
    answer = ask_rag(q, docs if docs else [""])

    # 3) Contexts trả về cho RAGAS đánh giá
    return answer, docs

# ====== Xây dựng EvaluationDataset ======
dataset = []
for q, ref in zip(sample_queries, expected_responses):
    ans, ctxs = answer_and_contexts(q)
    dataset.append(
        {
            "user_input": q,
            "retrieved_contexts": ctxs,
            "response": ans,
            "reference": ref,
        }
    )

evaluation_dataset = EvaluationDataset.from_list(dataset)

# Giải phóng cache nếu có GPU
try:
    torch.cuda.empty_cache()
except Exception:
    pass

# ====== Dùng Ollama làm LLM evaluator qua LangChain wrapper ======
eval_llm = OllamaLLM(
    model=MODEL_NAME,
    temperature=0
)

eval_llm = SafeOllamaWrapper(model=MODEL_NAME, temperature=0)
evaluator_llm = LangchainLLMWrapper(eval_llm)


# ====== Hàm evaluate an toàn cho nhiều phiên bản RAGAS ======
def evaluate_safe(dataset, metrics, llm):
    try:
        return evaluate(
            dataset=dataset,
            metrics=metrics,
            llm=llm,
            batch_size=1,
        )
    except TypeError:
        return evaluate(
            dataset=dataset,
            metrics=metrics,
            llm=llm
        )

# ====== Thực thi đánh giá ======
results = evaluate_safe(
    dataset=evaluation_dataset,
    metrics=[Faithfulness(), AnswerRelevancy(), ContextPrecision(), ContextRecall()],
    llm=evaluator_llm
)

print("\n=== RAGAS RESULTS ===")
print(results)
try:
    print(results.to_pandas())
except Exception:
    pass# ====== Dùng Ollama làm LLM evaluator qua LangChain wrapper ======
eval_llm = OllamaLLM(
    model=MODEL_NAME,
    temperature=0
)
evaluator_llm = LangchainLLMWrapper(eval_llm)