import json
from app.llm.chat import ask_llm
from app.graph_rag.collections import graph
from app.graph_rag._utils import render_prompt

def extract_entities(text):
    prompt = render_prompt("prompts/extract_entities.txt", text=text)
    response = ask_llm(prompt)
    return response.strip() 

def search_graph(graph, user_question):
    try:
        entities = extract_entities(user_question)
    except Exception as e:
        print(f"Error extracting entities: {e}")
        return []

    if not entities:
        return []
    
    print(entities)
    
    matched_nodes  = []
    for entity in entities:
        similar_nodes = graph.get_similar_nodes(entity)
        matched_nodes.extend(similar_nodes)
    
    unique_nodes = []
    seen = set()

    for node in matched_nodes:
        if node not in seen:
            unique_nodes.append(node)
            seen.add(node)
    
    print(f"unique_nodes: {unique_nodes}")
    
    sentences = []
    for node in unique_nodes:
        triples = graph.search_triples_with_depth(node, depth=1)
        for triple in triples:
            sentences.append(f"{triple[0]} {triple[1]} {triple[2]}")

    return sentences

