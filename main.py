from app.llm.chat import ask_rag
from app.vector_rag.collections import COLLECTIONS
from app.graph_rag.collections import graph
from app.graph_rag.retriever import search_graph


def run_pipeline(user_question):
    vector_rag_results = COLLECTIONS["phones"].search(user_question)
    graph_rag_results = search_graph(graph, user_question)
    documents = vector_rag_results + graph_rag_results
    return ask_rag(user_question, documents)


if __name__ == "__main__":
    graph.load("cache/entity_graph.pkl")
    print(run_pipeline("Hiện tại cửa hàng có những mẫu điện thoại nào phù hợp để học tập?"))