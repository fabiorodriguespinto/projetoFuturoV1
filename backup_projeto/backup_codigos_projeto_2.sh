#!/usr/bin/env bash
set -euo pipefail

# Diretório do projeto (pode ser passado como argumento)
PROJ_DIR="${1:-$(pwd)}"

# Diretório de backup do projeto
PROJ_BKP_DIR="/opt/Projetos/Projeto_FuturoV1/backup_projeto"

# Vai pro diretório do projeto
cd "$PROJ_DIR" || { echo "Erro: diretório $PROJ_DIR não encontrado"; exit 1; }

# Timestamp e arquivo de saída
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUT_FILE="${PROJ_BKP_DIR}/Projeto_FuturoV1_${TIMESTAMP}.txt"

# Lista de exclusões: podem ser diretórios (node_modules), arquivos (secrets.txt)
# ou padrões com wildcard (*.pyc). Adicione o que quiser aqui.
IGNORAR=(
  ".git"
  "node_modules"
  "__pycache__"
  "*.pyc"
  "*.log"
  "secrets.txt"
  "backup_projeto"
  "venv"
  "*.pkl"
  ".data"
)

# --- montar string para tree (-I expects pattern1|pattern2|...) ---
# Transformar IGNORAR em padrão do tree (separador '|')
TREE_PATTERNS=""
for item in "${IGNORAR[@]}"; do
  # escape de caractere '|' não necessário dentro das aspas, só juntar
  if [ -z "$TREE_PATTERNS" ]; then
    TREE_PATTERNS="$item"
  else
    TREE_PATTERNS="${TREE_PATTERNS}|${item}"
  fi
done

# --- montar expressão para find: \( -path "./a" -o -name "*.pyc" ... \) -prune -o -type f -print ---
FIND_EXPR=""
first=true
for item in "${IGNORAR[@]}"; do
  # se item contém wildcard '*' use -name, senão use -path para cobrir diretórios e arquivos
  if [[ "$item" == *'*'* || "$item" == *'?'* || "$item" == *'['* ]]; then
    # padrão com glob
    if $first; then
      FIND_EXPR="-name \"$item\""
      first=false
    else
      FIND_EXPR="${FIND_EXPR} -o -name \"$item\""
    fi
  else
    # sem wildcard: podemos querer excluir ./nome e tudo abaixo -> -path "./nome" -o -path "./nome/*"
    if $first; then
      FIND_EXPR="-path \"./$item\" -o -path \"./$item/*\""
      first=false
    else
      FIND_EXPR="${FIND_EXPR} -o -path \"./$item\" -o -path \"./$item/*\""
    fi
  fi
done

# --- Escreve cabeçalho no arquivo de saída ---
{
  echo "=============================="
  echo "📁 Estrutura de diretórios :: $PROJ_DIR"
  echo "Gerado: $(date --rfc-3339=seconds 2>/dev/null || date)"
  echo "=============================="
  echo ""
} > "$OUT_FILE"

# 1) Gera tree (ocultando padrões)
# se TREE_PATTERNS vazio, usa tree normalmente
if [ -n "$TREE_PATTERNS" ]; then
  # -a mostra arquivos ocultos; -I recebe expressão separada por '|'
  # usamos eval para interpretar corretamente a variável com barras e pipes
  eval tree -a -I "\"$TREE_PATTERNS\"" . >> "$OUT_FILE" 2>/dev/null || {
    # se tree não estiver instalado, cai aqui — faz fallback com find estrutural simples
    echo "(tree não instalado; mostrando lista com find)" >> "$OUT_FILE"
    eval find . \( $FIND_EXPR \) -prune -o -type d -print | sed 's|[^/]*/||g' >> "$OUT_FILE"
  }
else
  tree -a . >> "$OUT_FILE" 2>/dev/null || echo "(tree não instalado)" >> "$OUT_FILE"
fi

# separador
{
  echo ""
  echo "=============================="
  echo "📄 Conteúdo dos arquivos"
  echo "=============================="
  echo ""
} >> "$OUT_FILE"

# 2) Para cada arquivo: listar caminho e conteúdo
# Usar find com prune para excluir diretórios e padrões. Usar -print0 para nomes com espaços.
# Expressão final: find . \( <FIND_EXPR> \) -prune -o -type f -print0
# Como FIND_EXPR contém aspas, usamos eval com atenção.
eval "find . \\( $FIND_EXPR \\) -prune -o -type f -print0" | while IFS= read -r -d '' file; do
  {
    echo "----------------------------------------"
    echo "Arquivo: $file"
    echo "----------------------------------------"
  } >> "$OUT_FILE"

  # tentar detectar se o arquivo é texto; se texto imprime, se binário avisa
  # grep -Iq '.' retorna 0 para arquivos texto (não produz saída)
  if grep -Iq . "$file" 2>/dev/null; then
    # imprimir conteúdo
    cat "$file" >> "$OUT_FILE" 2>/dev/null || echo "[Erro lendo arquivo]" >> "$OUT_FILE"
  else
    echo "[BINÁRIO OU NÃO-TEXTO - conteúdo não incluído]" >> "$OUT_FILE"
  fi

  echo -e "\n" >> "$OUT_FILE"
done

echo "✅ Arquivo gerado: $PROJ_DIR/$OUT_FILE"
