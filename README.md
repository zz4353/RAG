# RAG

1. Qdrant

```cmd
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

2. Neo4j

```cmd
docker run -d --name neo4j -p7474:7474 -p7687:7687 -e NEO4J_AUTH=neo4j/test1234 neo4j:5
```

3. Ollama

```cmd
ollama serve &
ollama run gemma3:1b
```

4. Cài đặt

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

4. Run

```cmd
python main.py
```
