import os
import pickle
import numpy as np
from langchain_community.graphs.networkx_graph import NetworkxEntityGraph, KnowledgeTriple
from app.db.qdrant import VectorStore

class EmbeddingEntityGraph(NetworkxEntityGraph):
    def __init__(self, dense_model, collection_name):
        super().__init__()
        self.node_set = set()
        self.collection_name = collection_name  
        self.vector_store = VectorStore(self.collection_name, dense_model)

    def add_triple(self, subject, predicate, object_):
        super().add_triple(KnowledgeTriple(subject, predicate, object_))
        
        for node in [subject, object_]:
            if node not in self.node_set:
                self.vector_store.insert_data(
                    payload_keys=["node"],
                    payload_values=[[node]]
                )
                self.node_set.add(node)

    def get_similar_nodes(self, query, top_k=2, threshold=0.8):
        result = self.vector_store.search_dense(query, top_k=top_k, threshold=threshold)
        return [item.payload['node'] for item in result]
    
    def search_triples_with_depth(self, entity, depth=1):
        if entity not in self._graph:
            return []

        visited = set()
        queue = [(entity, 0)]
        triples = []

        while queue:
            current, cur_depth = queue.pop(0)
            if cur_depth >= depth or current in visited:
                continue
            visited.add(current)
            # Duyệt các node kề (chiều outbound)
            for neighbor in self._graph.successors(current):
                relation = self._graph[current][neighbor]['relation']
                triples.append((current, relation, neighbor))
                queue.append((neighbor, cur_depth + 1))

            for predecessor in self._graph.predecessors(current):
                relation = self._graph[predecessor][current]['relation']
                triples.append((predecessor, relation, current))
                queue.append((predecessor, cur_depth + 1))

        return triples
    
    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'wb') as f:
            pickle.dump({
                'graph': self._graph,
                'node_set': self.node_set,
                'collection_name': self.collection_name
            }, f)
        print(f"Graph saved to {path}")

    def load(self, path):
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self._graph = data['graph']
            self.node_set = data['node_set']
            self.collection_name = data['collection_name']
            self.vector_store = VectorStore(self.collection_name, self.vector_store.dense_embedding_model)
        print(f"Graph loaded from {path}")
    
    def recreate(self):
        self._graph.clear()
        self.node_set = set()
        self.vector_store.recreate_collection()

        

