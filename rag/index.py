# rag/index.py
import os
from rag.config import INDEX_PATHS, EXTENSIONS, INDEX_DIR

from llama_index.core import (
    VectorStoreIndex,
    Settings,
    StorageContext,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.schema import Document

def index_documents():
    docs = []

    for path in INDEX_PATHS:
        for root, _, files in os.walk(path):
            for file in files:
                if any(file.endswith(ext) for ext in EXTENSIONS):
                    full_path = os.path.join(root, file)
                    try:
                        print(f"📄 Lendo: {full_path}")
                        with open(full_path, encoding='utf-8') as f:
                            content = f.read()
                            if content.strip():
                                docs.append(content)
                    except Exception as e:
                        print(f"❌ Erro ao ler {full_path}: {e}")

    if not docs:
        print("⚠️ Nenhum documento encontrado para indexar.")
        return

    # Embedding local com modelo da Hugging Face
    Settings.embed_model = HuggingFaceEmbedding(model_name="all-MiniLM-L6-v2")

    documents = [Document(text=d) for d in docs]
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=str(INDEX_DIR))
    print(f"✅ Índice gerado com {len(documents)} documentos.")
