import json
from app.llm.chat import ask_llm
from app.graph_rag.collections import graph
from app.graph_rag._utils import render_prompt

def extract_entities(text):
    prompt = render_prompt("prompts/extract_entities.txt", text=text)
    response = ask_llm(prompt)
    return response.strip() 