import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load biến môi trường từ file .env (nếu có)
load_dotenv()

# Lấy các biến môi trường cần thiết
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Kiểm tra các biến đã được load chưa
if not NEO4J_URI or not NEO4J_USER or not NEO4J_PASSWORD:
    raise ValueError("Thiếu thông tin cấu hình Neo4j. Hãy kiểm tra file .env.")

# Tạo driver kết nối Neo4j
graph = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# --- Hàm ví dụ chạy query ---
def run_query(query, parameters=None):
    with graph.session() as session:
        result = session.run(query, parameters or {})
        return [record for record in result]

# --- Hàm đóng kết nối (nên gọi khi app kết thúc) ---
def close_graph():
    if graph is not None:
        graph.close()

# --- Ví dụ sử dụng ---
if __name__ == "__main__":
    query = "MATCH (n) RETURN n LIMIT 5"
    for record in run_query(query):
        print(record)
    close_graph()
