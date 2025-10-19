# <<<<<<< HEAD
from fastapi import FastAPI, Query, Request, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from app.db.qdrant import QDRANT_CLIENT
from app.src.api.chat import *
from app.vector_rag.indexer import load_and_index_data

from app.llm.chat import ask_rag
from app.vector_rag.collections import COLLECTIONS
from app.graph_rag.collections import graph
from app.graph_rag.retriever import search_graph

app = FastAPI(title="rag enpoit", version="0.1.0")

# Allow frontend dev server
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

def main():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    print("http://localhost:8000/docs")
    print("http://localhost:6333/dashboard#/collections")
    
def run_pipeline(user_question):
    vector_rag_results = COLLECTIONS["phones"].search(user_question)
    graph_rag_results = search_graph(graph, user_question)
    print(f"graph rag search :{graph_rag_results}")
    documents = vector_rag_results + graph_rag_results
    return ask_rag(user_question, documents)

if __name__ == "__main__":
    # Use the configured books collection.
    store = COLLECTIONS["phones"]
    data_dir = "/home/quyen/Documents/RAG_PROJECT/RAG/data/data"
    collection_name = store.collection_name
    
    # If collection exists, skip indexing; otherwise create/index
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
        
    graph.load("cache/entity_graph.pkl")
    # print("Start check graph collection ...")
    # graph_collection_name = "entity_graph_nodes"
    # if QDRANT_CLIENT.collection_exists(graph_collection_name):
    #     try:
    #         stats = QDRANT_CLIENT.count(graph_collection_name, exact=True)
    #         if getattr(stats, "count", 0) == 0:
    #             print(f"Graph collection '{graph_collection_name}' is empty. Graph may need reindexing...")
    #     except Exception as e:
    #         print(f"Could not check graph collection count ({e})")
    # try: 
    #     graph.load("cache/entity_graph.pkl")
    # except Exception as e:
    #     print(f"Could not load graph: {e}")
    print(run_pipeline("Hiện tại cửa hàng có những mẫu điện thoại nào phù hợp để học tập?"))
    main()
# =======
# from app.llm.chat import ask_rag
# from app.vector_rag.collections import COLLECTIONS
# from app.graph_rag.collections import graph
# from app.graph_rag.retriever import search_graph


# def run_pipeline(user_question):
#     vector_rag_results = COLLECTIONS["phones"].search(user_question)
#     graph_rag_results = search_graph(graph, user_question)
#     documents = vector_rag_results + graph_rag_results
#     return ask_rag(user_question, documents)


# if __name__ == "__main__":
#     graph.load("cache/entity_graph.pkl")
#     print(run_pipeline("Hiện tại cửa hàng có những mẫu điện thoại nào phù hợp để học tập?"))
# >>>>>>> origin/dev
