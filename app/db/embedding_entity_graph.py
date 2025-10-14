import pickle
import faiss
import numpy as np
from langchain_community.graphs.networkx_graph import NetworkxEntityGraph, KnowledgeTriple

class EmbeddingEntityGraph(NetworkxEntityGraph):
    def __init__(self, dense_model):
        super().__init__()
        self.node_list = []
        self.dense_embedding_model = dense_model
        self.faiss_index = faiss.IndexFlatIP(dense_model.get_dimension())

    def add_triple(self, subject, predicate, object_):
        super().add_triple(KnowledgeTriple(subject, predicate, object_))
        
        # Thêm embedding vào Faiss index nếu chưa tồn tại
        for node in [subject, object_]:
            if node not in self.node_list:
                emb = self.dense_embedding_model.encode(node)
                emb = np.array(emb).reshape(1, -1)
                emb = emb / np.linalg.norm(emb, axis=1, keepdims=True)  # Chuẩn hóa
                self.faiss_index.add(emb)
                self.node_list.append(node)

    def get_similar_nodes(self, query, top_k=2, threshold=0.85):
        query_emb = self.dense_embedding_model.encode(query)
        query_emb = np.array(query_emb).reshape(1, -1)
        query_emb = query_emb / np.linalg.norm(query_emb, axis=1, keepdims=True)

        D, I = self.faiss_index.search(query_emb, top_k)
        similar_nodes = []
        for dist, idx in zip(D[0], I[0]):
            if dist >= threshold:
                node = self.node_list[idx]
                similar_nodes.append(node)

        return similar_nodes
    
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
        with open(path, 'wb') as f:
            pickle.dump({
                'graph': self._graph,
                'node_list': self.node_list,
                'faiss_index': self.faiss_index
            }, f)
        print(f"Graph saved to {path}")

    def load(self, path):
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self._graph = data['graph']
            self.node_list = data['node_list']
            self.faiss_index = data['faiss_index']
        print(f"Graph loaded from {path}")
    

        

