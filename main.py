from fastapi import FastAPI, Query, Request, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from app.db.qdrant import QDRANT_CLIENT
from app.src.api.chat import *
from app.vector_rag.indexer import load_and_index_data

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

if __name__ == "__main__":
    # Use the configured books collection.
    store = COLLECTIONS["books"]
    data_dir = "/home/quyen/Documents/RAG_PROJECT/RAG/data/books"
    collection_name = store.collection_name
    
    # If collection exists, skip indexing; otherwise create/index
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
    main()