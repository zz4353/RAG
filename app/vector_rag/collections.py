from app.db.qdrant import VectorStore
from app.embedding.models import dense_model, sparse_model, cross_encoder

COLLECTIONS = {
    "phones": VectorStore(collection_name="phones_collection", dense_model=dense_model, sparse_model=sparse_model, cross_encoder=cross_encoder),
}