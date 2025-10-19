import json
from app.llm.chat import ask_llm
from app.graph_rag._utils import render_prompt
from app.graph_rag._utils import get_files_in_directory, load_file_as_markdown
from app.graph_rag.collections import graph
from app.graph_rag._utils import chunking

def preprocess_file(path):
    chunked_data = []

    # Xử lý file .docx, .txt và .pdf
    if path.endswith(".docx") or path.endswith(".pdf") or path.endswith(".txt"):
        print(f"Processing file: {path}")
        file_name = path.split("/")[-1]
        markdown_text = load_file_as_markdown(path)
        chunk_contents = chunking(markdown_text)
        chunked_data = [[chunk, file_name] for chunk in chunk_contents]
    elif path.endswith(".md"):
        file_name = path.split("/")[-1]

        with open(path, "r", encoding="utf-8") as f:
            markdown_text = f.read()

        chunk_contents = chunking(markdown_text)
        chunked_data = [[chunk, file_name] for chunk in chunk_contents]
    else:
        pass

    return chunked_data

def summarize_text(text):
    prompt = render_prompt("prompts/summarize_text.txt", text=text)
    response = ask_llm(prompt)
    return response.strip()

def extract_entities_and_relations(text):
    prompt = render_prompt("prompts/extract_entities_and_relations.txt", text=text)
    response = ask_llm(prompt)
    return json.loads(response.strip()) 

def load_and_index_data_to_graph(graph, data_path, save_path):
    graph.recreate()

    print(f"Indexing data from {data_path}...")
    files = get_files_in_directory(data_path)

    for path in files:
        print(path)
        chunked_data = preprocess_file(path)
        for chunk, source in chunked_data:
            try:
                doc = summarize_text(source + chunk)
            except Exception as e:
                print(f"Error summarizing text from {source}, {chunk}: {e}")
                continue

            try:
                triples = extract_entities_and_relations(doc)
            except Exception as e:
                print(f"Error extracting entities and relations from {source}, {chunk}: {e}")
                continue
            
            for triple in triples:
                graph.add_triple(triple["subject"], triple["relation"], triple["object"])
    graph.save(save_path)
    print("Done indexing.")

