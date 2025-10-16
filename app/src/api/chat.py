from fastapi import FastAPI, Query, Request, UploadFile, File, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
import requests
import os

from app.llm.chat import ask_llm, ask_rag
from app.vector_rag.collections import COLLECTIONS
from app.vector_rag.indexer import load_and_index_data
from app.src.models.models import *

router = APIRouter()

# Endpoints
@router.post("/ask-llm")
def ask_llm_enpoint(req: AskRequest)-> Dict:
    answer = ask_llm(req.question)
    return {"question": req.question, "answer": answer}

@router.post("/ask-rag")
def ask_rag_enpoint(req: RagRequest)-> Dict:
    req.docs = COLLECTIONS["books"].search(req.question, top_k=3, threshold=0.3) 
    answer = ask_rag(req.question, req.docs)
    return {"question": req.question, "docs": req.docs, "answer": answer}

@router.api_route("/index", methods=["GET", "POST"])
def index_data(req: IndexRequest, request: Request = None)-> Dict:
    if req.collection_name not in COLLECTIONS:
        return {"error": f"Collection {req.collection_name} not found."}
    if request.method == "GET":
        return {"message": "Use POST with JSON body to index data, e.g. {'collection_name': 'books', 'data_path': 'data/books'}"}
    load_and_index_data(COLLECTIONS[req.collection_name], req.data_path)
    return {"status": "success", "index_path": req.data_path, "collection_name": req.collection_name}


@router.post("/search")
def search_docs(req: SearchRequest)-> Dict:
    if req.collection_name not in COLLECTIONS:
        return {"error": f"Collection {req.collection_name} not found."}
    docs = COLLECTIONS[req.collection_name].search(
        req.query, top_k=req.top_k, threshold=req.threshold
    )
    return {"query": req.query, "result": docs}


@router.get("/", response_model=HealthRespond)
def root() -> HealthRespond:
    def check_qdrant():
        try:
            requests.get("http://localhost:6333/dashboard")
            return "qdrant is healthy."
        except Exception as e:
            return e
        

    def check_ollama():
        try:
            requests.get("http://localhost:11434/api/tags", timeout=3) 
            return f"ollama model is healthy."
        except Exception as e:
            return e

    def check_collections():
        status = {"keys": str(COLLECTIONS.keys()), "value": str(COLLECTIONS.values())}
        return status

    overal = HealthRespond(
        status="False",
        backend="running",
        qdrant=check_qdrant(),
        ollama=check_ollama(),
        collections=check_collections()
    )
    return overal


@router.get("/collections")
def get_collections() -> Dict:
    collections_info = []
    # print(COLLECTIONS.items())
    for name, collection in COLLECTIONS.items():
        info = collection.get_collection_info()
        collections_info.append({
            "name": name,
            "count": info.points_count,
            "status": "activate"
        })
    return {"collections": collections_info}


# @router.post("/upload")
# async def upload_files(files: List[UploadFile] = File(...)) -> Dict:
#     """Upload files and index into the default 'books' collection."""
#     try:
#         upload_dir = os.path.join("data", "books")
#         os.makedirs(upload_dir, exist_ok=True)

#         saved_files: List[str] = []
#         for f in files:
#             dest_path = os.path.join(upload_dir, f.filename)
#             content = await f.read()
#             with open(dest_path, "wb") as out:
#                 out.write(content)
#             saved_files.append(dest_path)

#         # Index the directory after saving
#         load_and_index_data(COLLECTIONS["books"], upload_dir)

#         return {
#             "status": "success",
#             "files_processed": len(saved_files),
#             "saved": saved_files,
#         }
#     except Exception as e:
#         return {"status": "error", "error": str(e)}