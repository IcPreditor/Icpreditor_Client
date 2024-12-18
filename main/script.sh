#!/bin/bash
#Script Inicializador

# Caminho para o arquivo que armazenará o valor de KEEP_SESSION
CONFIG_FILE="./keep_session_config.txt"

# valor default KEEP_SESSION=false, pede login
# se valor for true e tiver o arquivo token.json, não solicita o login.
# $python_cmd ../dataGenerator/genStudents.py se  esse comando retornar erro no arquivo





# # Função para perguntar ao usuário e armazenar o valor de KEEP_SESSION
# ask_keep_session() {
#     if [[ "$resposta" == "sim" ]]; then
#         echo "Sessão de login será mantida."
#     elif [[ "$resposta" == "nao" ]]; then
#         echo "KEEP_SESSION=nao" > "$CONFIG_FILE"
#         echo "Sessão de login não será mantida."
#     else
#         echo "Resposta inválida. Tente novamente."
#         ask_keep_session
#     fi
# }

# # Verifica se o arquivo de configuração existe
# if [[ -f "$CONFIG_FILE" ]]; then
#     # Lê o valor de KEEP_SESSION do arquivo
#     source "$CONFIG_FILE"
#     echo "Configuração encontrada: KEEP_SESSION=$KEEP_SESSION"
# else
#     # Pergunta ao usuário caso seja a primeira execução
#     echo "Configuração de KEEP_SESSION não encontrada."
#     ask_keep_session
# fi

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
	pip install -r requirements.txt
	echo "Instalação concluída!"
else 
	echo "Instalação cancelada pelo usuário."
	exit 1
fi
echo "Fazendo login"
$python_cmd ../dataGenerator/tokenCheck.py

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


