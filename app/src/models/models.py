from pydantic import BaseModel
from typing import List, Dict

class AskRequest(BaseModel):
    question: str
    
class RagRequest(BaseModel):
    question: str
    docs: List[str]


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