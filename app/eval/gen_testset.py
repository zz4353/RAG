import os
from pathlib import Path
from typing import Dict, List
import json

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

# CONFIG PATH, LLM, ...
dir_path = Path(os.path.dirname(__file__))
out_json= os.path.join(dir_path, "test_set.json")
data_path = os.path.join(dir_path.parent.parent, "data/data")
MODEL_NAME = "gpt-4o-mini"
TEMPERATURE = 0
MAX_TOKENS = 800
QAS_PER_FILE = 3
OPENAI_KEY = os.getenv("OPENAI_API_KEY","")


# edit prompt
def prompt_init(doc_text: str, n_qas: int) -> str:
    print(f"Start to construct promt ...")
    return f"""
Imagine you are a phone consultant and also a customer. With the document below, create {n_qas} high-quality Vietnamese QA pairs to evaluate the RAG system.

Rules:
- ONLY answer the questions in the given document.

- Answers must be clear, concise, well-founded and in Vietnamese.

- Prioritize diverse types of questions (who is the machine suitable for?, what are the machine's specifications?; how much does it cost?; color; size;...).

- Export as JSON with the schema: {{"qas":[{{"question": "...","answer":"..."}}, ...]}}

Document:
\"\"{doc_text[:8000]}\"\"\"
"""

def call_llm(llm: ChatOpenAI, prompt: str) -> Dict:
    print(f"Start call {MODEL_NAME} ...")
    resp = llm.invoke(prompt)
    text = resp.content.strip()
    # Remove ```json and ``` if present
    if text.startswith("```"):
        # remove the first line
        text = "\n".join(text.split("\n")[1:])
    if text.endswith("```"):
        text = text[: -3]
    text = text.strip()
    data = json.loads(text)
    return data

def load_text(path: Path) -> str:
    print(f"Start to load text from {path} ...")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_json(items: List[Dict], out_path: str) -> None:
    """Ghi toàn bộ dữ liệu thành 1 file JSON hợp lệ."""
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def main():

    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=MODEL_NAME,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )
    
    list_md_files = [f for f in os.listdir(data_path) if f.endswith("md")]
    jsonl_rows = []
    
    for i, file_name in enumerate(list_md_files, 1):
        doc_path = os.path.join(data_path, file_name)
        text_doc = load_text(doc_path)
        prompt = prompt_init(text_doc, QAS_PER_FILE)
        
        data = call_llm(llm, prompt)
        
        qas = []
        for qa in data.get("qas", []):
            question = (qa.get("question"))
            answer = (qa.get("answer"))
            if question and answer:
                qas.append({"question": question, "answer": answer})
        print(qas)
        
        jsonl_rows.append({
            "source": str(file_name),
            "qas": qas,
        })
        print("done")
        if i == 100:
            break
    # write_jsonl(jsonl_rows, out_json)
    write_json(jsonl_rows, out_json)


if __name__ == "__main__":
    main()
