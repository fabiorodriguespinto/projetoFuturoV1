#!/bin/bash

#projeto_dir="/opt/Projetos/Projeto_FuturoV1"


#timestamp=$(date +"%Y%m%d_%H%M%S")


# Diretório do projeto (pode ser passado como argumento)
PROJ_DIR="${1:-$(pwd)}"

# Diretório de backup do projeto
PROJ_BKP_DIR="/opt/Projetos/Projeto_FuturoV1/backup_projeto"

# Diretório atual
cd "$PROJ_DIR" || { echo "Erro: diretório $PROJ_DIR não encontrado"; exit 1; }

# Timestamp e nome do arquivo de saída
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUT_FILE="${PROJ_BKP_DIR}/Projeto_FuturoV1_${TIMESTAMP}.txt"

# Diretórios/arquivos a ignorar (adicione conforme necessário)
IGNORAR=(
  ".git"
  "__pycache__"
  "node_modules"
  "*.pyc"
  "*.log"
  ".data"
  "backup_projeto"
  "venv"
  "*.pkl"
)

# Converter lista de exclusões em parâmetros do tree e find
TREE_IGNORE=""
FIND_IGNORE=""

for item in "${IGNORAR[@]}"; do
  TREE_IGNORE+=" -I '$item'"
  FIND_IGNORE+=" ! -path \"*/$item/*\""
done

# 1️⃣ Gera estrutura de diretórios (tree)
echo "==============================" > "$OUT_FILE"
echo "📁 Estrutura de diretórios" >> "$OUT_FILE"
echo "==============================" >> "$OUT_FILE"
echo "" >> "$OUT_FILE"

# Executa tree com filtros (usa eval para interpretar variáveis com aspas)
eval tree -a $TREE_IGNORE . >> "$OUT_FILE"

echo "" >> "$OUT_FILE"
echo "==============================" >> "$OUT_FILE"
echo "📄 Conteúdo dos arquivos" >> "$OUT_FILE"
echo "==============================" >> "$OUT_FILE"
echo "" >> "$OUT_FILE"

# 2️⃣ Para cada arquivo, salva caminho e conteúdo
# Usa find com exclusões e lê apenas arquivos normais
eval find . -type f $FIND_IGNORE | while read -r file; do
  echo "----------------------------------------" >> "$OUT_FILE"
  echo "Arquivo: $file" >> "$OUT_FILE"
  echo "----------------------------------------" >> "$OUT_FILE"
  cat "$file" >> "$OUT_FILE" 2>/dev/null
  echo -e "\n\n" >> "$OUT_FILE"
done

# 3️⃣ Mensagem final
echo "✅ Arquivo gerado: $OUT_FILE"

