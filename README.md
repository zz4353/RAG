# RAG

1. Chạy các database

```cmd
docker compose up -d
```

2. Ollama

```cmd
ollama serve &
ollama run gemma3:1b
```

3. Cài đặt

- Sử dụng python:

```cmd
git clone https://github.com/zz4353/RAG.git
cd RAG
pip install -r requirements.txt
```

- Sử dụng miniconda:

```cmd
git clone https://github.com/zz4353/RAG.git
cd RAG
conda create -n rag python=3.10
conda activate rag
pip install -r requirements.txt
```

4. Lấy data và index data

- Chạy 
```cmd
chmod +x data.sh &
bash data.sh
```

5. Run

```cmd
python main.py
```

6. Hướng dẫn chạy dự án.
```text
- vào thư mục root của dự án sau đó chạy: docker compose up
- chạy main.py để chạy backend và check vectordb và graphdb nếu không có sẽ tự động được load và khởi tạo: python -m main
- chay frontend: npm run dev
- truy cap vao: http://localhost:5173/
```

7. Huong dan danh gia.
```text
- vao root
- Trong gen_testset.py Dieu chinh QAS_PER_FILE de gioi han so cau hoi danh gia duoc sinh ra tren tai lieu
- chay gen_testset.py de sinh test_set.json: python -m app.eval.gen_testset
- chay eval.py de danh gia hybird va rag only: python -m app.eval.eval
```
