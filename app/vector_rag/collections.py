from app.db.qdrant import VectorStore
from app.embedding.models import DenseEmbedding

dense_model = DenseEmbedding()

COLLECTIONS = {
    "books": VectorStore(collection_name="books_collection", dense_model=dense_model),
}