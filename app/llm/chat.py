import os
from app.llm.llm_integrations import get_llm
from app.llm._utils import render_prompt

def ask_llm(prompt):
    response = get_llm().invoke(prompt)
    if isinstance(response, str):
        return response
    return response.content

# def ask_rag(prompt, documents):
#     prompt = render_prompt(os.path.join(os.path.realpath(__file__),"..", "prompts", "prompt.txt"), documents, prompt)
#     return ask_llm(prompt)

def ask_rag(prompt, documents):
    base_dir = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(base_dir, "prompts", "prompt.txt")
    prompt = render_prompt(template_path, documents, prompt)
    return ask_llm(prompt)