from fastapi import FastAPI, Query, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.src.api.chat import *

app = FastAPI(title="rag enpoit", version="0.1.0")

# Allow frontend dev server
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

def main():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    print("http://localhost:8000/docs")
    print("http://localhost:6333/dashboard#/collections")

if __name__ == "__main__":
    main()