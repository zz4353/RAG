import json
from app.db.qdrant import VectorStore, QDRANT_CLIENT
from qdrant_client.models import PointStruct
from app.graph_rag.collections import graph
from app.vector_rag.collections import dense_model, sparse_model, cross_encoder
from app.vector_rag.indexer import load_and_index_data
from app.vector_rag.collections import COLLECTIONS

try:
    QDRANT_CLIENT.delete_collection("entity_graph_nodes")
except:
    pass

try:
    QDRANT_CLIENT.delete_collection("phones")
except:
    pass

graph.load("cache/entity_graph.pkl")

z = VectorStore("entity_graph_nodes", dense_model, sparse_model, cross_encoder)

nodes = list(graph._graph.nodes())

print("Inserting 1")
z.insert_data(payload_keys=["node"], payload_values=nodes)
print("Insertion done.")

print("Inserting 2")
load_and_index_data(COLLECTIONS["phones"], "data") 
print("Insertion done.")