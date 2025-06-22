from pathlib import Path

# Diretórios a serem indexados (agora usando resolve para garantir caminhos absolutos)
BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_PATHS = [
    BASE_DIR / "api",
    BASE_DIR / "worker",
    BASE_DIR / "nn",
    BASE_DIR / "shared"
]

# Tipos de arquivos suportados
EXTENSIONS = [".py", ".md", ".txt"]

# Diretório de armazenamento de índice e dados
INDEX_DIR = Path("./storage")
DOCS_DIR = Path("./docs")
