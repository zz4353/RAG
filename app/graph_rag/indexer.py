import json
from app.llm.chat import ask_llm
from app.graph_rag.collections import graph
from app.graph_rag._utils import render_prompt

def extract_entities_and_relations(text):
    prompt = render_prompt("prompts/extract_entities_and_relations.txt", text=text)
    response = ask_llm(prompt)
    return json.loads(response.strip()) 

def summarize_text(text):
    prompt = render_prompt("prompts/summarize_text.txt", text=text)
    response = ask_llm(prompt)
    return response.strip()


