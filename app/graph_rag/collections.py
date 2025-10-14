from app.db.embedding_entity_graph import EmbeddingEntityGraph
from app.embedding.models import DenseEmbedding

dense_model = DenseEmbedding()

graph = EmbeddingEntityGraph(dense_model)
