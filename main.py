# from app.llm.chat import ask_llm, ask_rag
# from app.vector_rag.indexer import load_and_index_data
# from app.vector_rag.collections import COLLECTIONS

# question = "Xin chào, bạn là mô hình gì?"
# answer = ask_llm(question)
# print(answer)
# print("--------------------------------------------------------")

# question = "Con vịt có mấy chân?"
# docs = ["Con vịt có 4 chân."]
# answer = ask_rag(question, docs)
# print(answer)
# print("--------------------------------------------------------")

# load_and_index_data(COLLECTIONS["books"], "data/books")  # index data xong thì comment lại.

# question = "phụ nữ muốn gì ở đàn ông?"
# docs = COLLECTIONS["books"].search(question, top_k=3, threshold=0.3)
# print(docs)
# print("--------------------------------------------------------")

# answer = ask_rag(question, docs)
# print(answer)


from app.graph_rag.indexer import extract_entities_and_relations
text = "Hà Nội là thủ đô của Việt Nam. Hồ Chí Minh là thành phố lớn nhất Việt Nam. Hà Nội nổi tiếng với ẩm thực và văn hóa phong phú."
response = extract_entities_and_relations(text)
print(response)