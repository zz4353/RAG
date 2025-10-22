from fastapi import FastAPI, Query, Request, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from app.db.qdrant import QDRANT_CLIENT
from app.src.api.chat import *
from app.vector_rag.indexer import load_and_index_data

from app.llm.chat import ask_rag
from app.vector_rag.collections import COLLECTIONS
from app.graph_rag.collections import graph
from app.graph_rag.retriever import search_graph
import os
from pathlib import Path

app = FastAPI(title="rag enpoit", version="0.1.0")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.on_event("startup")
def startup_load_indexes():
    # Ensure vector collection
    store = COLLECTIONS["phones"]
    dir_path = Path(os.path.dirname(__file__)).parent  # project root of 'app'
    data_dir = os.path.join(dir_path, "data/data")
    collection_name = store.collection_name

    print("Start check data_chunk collection ...")
    if QDRANT_CLIENT.collection_exists(collection_name):
        try:
            stats = QDRANT_CLIENT.count(collection_name, exact=True)
            if getattr(stats, "count", 0) == 0:
                print(f"Collection '{collection_name}' exists but is empty. Indexing...")
                load_and_index_data(store, data_dir)
        except Exception as e:
            print(f"Could not check collection count ({e}). Proceeding to index...")
            load_and_index_data(store, data_dir)
    else:
        print(f"Collection '{collection_name}' not found. Creating and indexing...")
        load_and_index_data(store, data_dir)

    # Ensure graph and node vectors
    graph_file = "cache/entity_graph.pkl"
    graph_collection_name = "entity_graph_nodes"
    print("Start check graph collection ...")
    if QDRANT_CLIENT.collection_exists(graph_collection_name):
        try:
            graph.load(graph_file)
            stats = QDRANT_CLIENT.count(graph_collection_name, exact=True)
            if getattr(stats, "count", 0) == 0:
                print(f"Graph collection '{graph_collection_name}' is empty. Repopulating from pickle...")
                nodes = [[n] for n in getattr(graph, "node_set", set())]
                if nodes:
                    graph.vector_store.insert_data(payload_keys=["node"], payload_values=nodes)
                    print(f"Repopulated {len(nodes)} nodes into '{graph_collection_name}'.")
                else:
                    print("No nodes found in graph.node_set. You may need to reindex.")
        except Exception as e:
            print(f"Could not check graph collection count ({e})")

    try:
        graph.load(graph_file)
    except Exception as e:
        print(f"Could not load graph: {e}")

def main():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    print("http://localhost:8000/docs")
    print("http://localhost:6333/dashboard")

if __name__ == "__main__":
    main()