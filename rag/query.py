# rag/query.py
from llama_index.core import StorageContext, load_index_from_storage
from rag.config import INDEX_DIR

def consulta_usuario(pergunta: str):
    storage_context = StorageContext.from_defaults(persist_dir=str(INDEX_DIR))
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    resposta = query_engine.query(pergunta)
    print("💡 Resposta:")
    print(resposta)
