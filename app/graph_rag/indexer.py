import json
from app.llm.chat import ask_llm
from app.graph_rag._utils import render_prompt


def summarize_text(text):
    prompt = render_prompt("prompts/summarize_text.txt", text=text)
    response = ask_llm(prompt)
    return response.strip()

def extract_entities_and_relations(text):
    prompt = render_prompt("prompts/extract_entities_and_relations.txt", text=text)
    response = ask_llm(prompt)
    return json.loads(response.strip()) 

def load_and_index(graph, save_path, documents=[]):
    for doc in documents:
        doc = summarize_text(doc)
        triples = extract_entities_and_relations(doc)
        for triple in triples:
            graph.add_triple(triple["subject"], triple["relation"], triple["object"])
    graph.save(save_path)
    print("Done indexing.")

