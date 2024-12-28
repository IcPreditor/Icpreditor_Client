#!/bin/bash
#Script Inicializador

# Caminho para o arquivo que armazenará o valor de KEEP_SESSION
#CONFIG_FILE="./keep_session_config.txt"

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

#
config="configs.txt"
caminho_arquivo="../data/credentials.json"
caminho_requirements="../requirements.txt"
caminho_token="../data/token.json"

deleteTemp(){
	if [ -e $caminho_arquivo ]; then
		# Deleta credentials temporarias
		rm $caminho_arquivo
	fi
}
#Ask for Credentials
login(){
	echo 'Login Scao:'
	read login

	echo 'Senha:'
	read senha

	#cria arquivo de credentials (temporario)
	mkdir -p "$(dirname "$caminho_arquivo")"

	echo "{
	\"credentials\": {
		\"username\": \"$login\",
		\"password\": \"$senha\"
	}
	}" > "$caminho_arquivo"
}

#verifica python instalado
if command -v python3 &>/dev/null; then
	python_cmd="python3"
elif command -v python &>/dev/null; then
	python_cmd="python"
else
	echo "Erro: Nenhuma versão do Python foi encontrada"
	exit 1
fi
# verifica se requirements está presente 
if [ ! -f $caminho_requirements ]; then
    echo "Arquivo requirements.txt não encontrado!"
    exit 1
fi
#instalação de módulos necessários
echo "Conteúdo do requirements.txt:"
cat $caminho_requirements
read -p "Deseja instalar os módulos listados em requirements.txt ? (s/n)" resposta
#converter em minúsculo
resposta=${resposta,,}

if [[ "$resposta" == "s" || "$resposta" == "sim" || "$resposta" == "y" || "$resposta" == "yes" ]]; then
	# Execurtar o comando de instalação
	echo "Instalando os Módulos ..."
	$python_cmd -m pip install -r ../requirements.txt
	echo "Instalação concluída!"
else 
	echo "Instalação cancelada pelo usuário."
	deleteTemp
	exit 1
fi
#Config Keep Session
keep_session_config=$(grep "^keep_session=" "$config")
if [ -n $keep_session_config ]; then
	keep_session=${keep_session_config#*=}
fi

if [ $keep_session == "true" ]; then
	echo "Verificando Existencia de Token"
	if [ -e $caminho_token ]; then
		echo "Token encontrado"
		status_token=$($python_cmd ../dataGenerator/tokenCheck.py 1)
		echo "Verificando validade do Token"
		if [ $status_token == "error" ]; then
			echo "Token invalido, login necessário"
			login
		else
			echo "Token OK"
		fi
	else
		echo "Token não encontrado, login necessário"
		login
	fi
else
	echo "Login Necessário :"
	login
fi

deleteTemp

echo "Recuperando estudantes para treino da Regressão Logistica"
# gera estudantes para treino
$python_cmd ../dataGenerator/genStudents.py
echo "Estudantes de treino Recuperados"



#Config students By Course
byCourse_config=$(grep "^studentsByCourse=" "$config")
if [ -n $byCourse_config ]; then
	byCourse=${byCourse_config#*=}
fi

if [ $byCourse == "true" ]; then
	echo "Busca por curso"
	#Config codigo do curso
	courseId_config=$(grep "^cursoId=" "$config")
	if [ -n $courseId_config ]; then
		courseId=${courseId_config#*=}
		echo "Codigo de Curso: " $courseId
	fi
	#Config begin 
	inicio_config=$(grep "^periodoInicio=" "$config")
	if [ -n $inicio_config ]; then
		inicio=${inicio_config#*=}
		echo "Periodo de Inicio" $inicio
	fi
	#Config end 
	fim_config=$(grep "^periodoFim=" "$config")
	if [ -n $fim_config ]; then
		fim=${fim_config#*=}
		echo "Periodo de Fim" $fim
	fi
	# estudantes por codigo de curso 
	echo "Recuperando estudantes pelo curso configurado em configs.txt"
	$python_cmd ../dataGenerator/genStudentsByCourse.py $courseId $inicio $fim
else
	# estudantes em matricula.txt
	echo "Recuperando estudantes pela matricula em matriculas.txt"
	$python_cmd ../dataGenerator/getStudent.py 
fi

echo "Iniciando Regressão Logística"
# regressão logistica treinamento, teste e previsão
$python_cmd ../dataGenerator/regressaoLogistica.py 