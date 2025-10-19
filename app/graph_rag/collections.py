from app.db.embedding_entity_graph import EmbeddingEntityGraph
from app.embedding.models import dense_model

graph = EmbeddingEntityGraph(dense_model, collection_name="entity_graph_nodes")
