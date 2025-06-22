# rag/main.py
import argparse
from rag.index import index_documents
from rag.query import consulta_usuario

def main():
    parser = argparse.ArgumentParser(description="Pipeline RAG - LlamaIndex")
    parser.add_argument("--index", action="store_true", help="Indexar arquivos do projeto")
    parser.add_argument("--query", type=str, help="Fazer uma pergunta baseada no índice")

    args = parser.parse_args()

    if args.index:
        index_documents()

    if args.query:
        consulta_usuario(args.query)

if __name__ == "__main__":
    main()
