from pydantic import BaseModel
from typing import List, Dict, Any

class AskRequest(BaseModel):
    question: str
    
class RagRequest(BaseModel):
    question: str
    docs: List[str]
    
class HybridRequest(BaseModel):
    question: str
    docs_vectordb: List[str]
    sentences: List[str]
    
class CollectionInfo(BaseModel):
    name: str
    count: int
    status: str


class IndexRequest(BaseModel):
    collection_name: str
    data_path: str
    

class SearchRequest(BaseModel):
    collection_name: str
    query: str
    top_k: int = 3
    threshold: float = 0.3
    
class HealthRespond(BaseModel):
    status: str
    backend: str
    qdrant: str
    ollama: str
    collections: Dict[str, str]