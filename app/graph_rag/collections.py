from app.db.embedding_entity_graph import EmbeddingEntityGraph
from app.embedding.models import dense_model, sparse_model, cross_encoder

graph = EmbeddingEntityGraph(dense_model, sparse_model, cross_encoder, collection_name="entity_graph_nodes")
