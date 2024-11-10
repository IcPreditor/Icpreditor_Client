#!/bin/bash
#Script Inicializador

#Credentials
echo 'Login Scao:'
read login

echo 'Senha:'
read -s senha

caminho_arquivo="../data/credentials.json"
mkdir -p "$(dirname "$caminho_arquivo")"

echo "{
  \"credentials\": {
    \"username\": \"$login\",
    \"password\": \"$senha\"
  }
}" > "$caminho_arquivo"


# Verifica se python3 está disponível
if command -v python3 &>/dev/null; then
	python_cmd="python3"
elif command -v python &>/dev/null; then
	python_cmd="python"
else
	echo "Erro: Nenhuma versão do Python foi encontrada"
	exit 1
fi

$python_cmd main.py

if [ ! -f ../requirements.txt ]; then
    echo "Arquivo requirements.txt não encontrado!"
    exit 1
fi

echo "Conteúdo do requirements.txt:"
cat requirements.txt
read -p "Deseja instalar os módulos listados em requirements.txt ? (s/n)" resposta
#converter em minúsculo
resposta = ${resposta,,}

if [[ "$resposta" == "s" || "$resposta" == "sim" || "$resposta" == "y" || "$resposta" == "yes" ]]; then
	# Execurtar o comando de instalação
	echo "Instalando os Módulos ..."
	pip install requirements.txt
	echo "Instalação concluída!"
else 
	echo "Instalação cancelada pelo usuário."
	exit 1
fi
echo "Recuperando estudantes"
# gera estudantes para treino
$python_cmd ../dataGenerator/genStudents.py
# Deleta credentials após geração de token
rm ../data/credentials.json

echo "Recuperando estudantes pela matricula"
# estudantes para prever TO DO
$python_cmd ../dataGenerator/getStudent.py $1

echo "Iniciando Regressão Logística"
# regressão logistica treinamento, teste e previsão
$python_cmd ../data/dataGenerator/logisticRegression.py 


