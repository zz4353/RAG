from app.db.qdrant import VectorStore
from app.embedding.models import dense_model

COLLECTIONS = {
    "phones": VectorStore(collection_name="phones_collection", dense_model=dense_model),
}