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

from app.graph_rag.retriever import search_graph
from app.graph_rag.collections import graph

router = APIRouter()

# Endpoints
@router.post("/ask-llm")
def ask_llm_enpoint(req: AskRequest)-> Dict:
    answer = ask_llm(req.question)
    return {"question": req.question, "answer": answer}

@router.post("/ask-rag")
def ask_rag_endpoint(req: RagRequest) -> Dict:
    raw_docs = COLLECTIONS["phones"].search(req.question, top_k=3, threshold=0.3)
    print(raw_docs)
    answer = ask_rag(req.question, [d["content"] for d in raw_docs])

    return {
        "question": req.question,
        "docs": [
            {
                # "id": str(i),
                "payload": {"source": d["source"], "content": d["content"]},
                # "score": d.get("score", 0)
            }
            for i, d in enumerate(raw_docs)
        ],
        "answer": answer
    }

@router.post("/ask_hybrid")
def ask_hybrid_enpoint(req: HybridRequest) -> Dict:
    req.docs_vectordb = COLLECTIONS["phones"].search(req.question, top_k=3, threshold=0.3)

    raw_graph = search_graph(graph, req.question)
    # print(f"raw_graph: {raw_graph}")
    graph_docs = [{"source": "graph", "content": s} for s in raw_graph]
    req.sentences = graph_docs
    documents = req.docs_vectordb + req.sentences
    # print(req.docs_vectordb)
    # print("-----------------------------------------")
    # print(documents) # array of objects Là một object (đối tượng JSON-like) với exactly 2 keys: "content" và "source"
    answer = ask_rag(req.question, documents)
    return {
        "question": req.question,
        "docs": [
            {"payload": {"source": d["source"], "content": d["content"]},}for d in documents
        ],
        "answer": answer
    }

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


@router.get("/collections", response_model=Dict[str, List[CollectionInfo]])
def get_collections():
    collections_info = []
    for name, collection in COLLECTIONS.items():
        info = collection.get_collection_info()
        collections_info.append(
            CollectionInfo(
                name=name,
                count=info.points_count,
                status="activate"
            )
        )
    return {"collections": collections_info}


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


