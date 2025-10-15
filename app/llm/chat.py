import os
from app.llm.llm_integrations import get_llm
from app.llm._utils import render_prompt

def ask_llm(prompt):
    response = get_llm().invoke(prompt)
    if isinstance(response, str):
        return response
    return response.content

def ask_rag(prompt, documents):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    prompt_path = os.path.abspath(os.path.join(base_dir, "prompts", "prompt.txt"))
    prompt = render_prompt(prompt_path, documents, prompt)
    return ask_llm(prompt)