from langchain_community.graphs.networkx_graph import  KnowledgeTriple
from app.db.embedding_entity_graph import EmbeddingEntityGraph
from app.embedding.models import DenseEmbedding

# đảm bảo các triple, dữ liệu đều dạng lowercase
dense_model = DenseEmbedding()
graph = EmbeddingEntityGraph(dense_model)
# graph.add_triple("bread","produces","iphone 15")
# graph.add_triple("bread","z","zz 15")
# graph.add_triple("iphone 15","uses_chip","a17 pro")
# graph.add_triple("a17 pro","manufactured_by","tsmc")

graph.load("test_graph.pkl")

graph._graph.nodes()

print(graph.search_triples_with_depth("tsmc", depth=1))

graph.save("test_graph.pkl")