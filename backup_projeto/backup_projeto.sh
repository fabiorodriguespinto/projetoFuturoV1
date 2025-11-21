#!/bin/bash

projeto_dir="/opt/Projetos/Projeto_FuturoV1"

projeto_bkp_dir="/opt/Projetos/Projeto_FuturoV1/backup_projeto"

timestamp=$(date +"%Y%m%d_%H%M%S")

tree $projeto_dir -I venv -I backup_projeto -I __pycache__ > $projeto_bkp_dir/Projeto_FuturoV1_$timestamp.txt

echo ""
