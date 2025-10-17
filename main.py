from app.llm.chat import ask_rag
from app.vector_rag.collections import COLLECTIONS
from app.vector_rag.indexer import load_and_index_data
from app.graph_rag.collections import graph
from app.graph_rag.indexer import load_and_index_data_to_graph
from app.graph_rag.retriever import search_graph


# Chỉ chạy 1 lần để index dữ liệu vào collection vector store
# load_and_index_data(COLLECTIONS["phones"], "data") 

# Chỉ chạy 1 lần để index dữ liệu vào graph
# load_and_index_data_to_graph(graph, "data", "cache/entity_graph.pkl") 

def run_pipeline(user_question):
    vector_rag_results = COLLECTIONS["phones"].search(user_question)
    graph_rag_results = search_graph(graph, user_question)
    documents = vector_rag_results + graph_rag_results
    return ask_rag(user_question, documents)


if __name__ == "__main__":
    graph.load("cache/entity_graph.pkl")
    print(run_pipeline("Điện thoại pin trâu, chụp ảnh đẹp trong tầm giá 5 triệu"))