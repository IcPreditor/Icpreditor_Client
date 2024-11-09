#python3
#Generates .json with a student
#Uses requests to the eureca ufcg system, 
#with  the token in token.json
#Guilherme Fernandes, 2024
import sys
import requests as req
import pandas as pd
import json

url_token = 'https://eureca.sti.ufcg.edu.br/as'
url_eureca= 'https://eureca.sti.ufcg.edu.br/das/v2'



#request profile (using token)
def getProfile(token):
    headers = {'content-type':'application/json',"token-de-autenticacao":token}
    request = req.get((url_token+"/profile"),headers=headers)
    return request.json()

#student by course // 2017.1-2023.2
def saveStudent(token,matricula):
    headers = {'content-type':'application/json',"token-de-autenticacao":token}
    request = req.get(url_eureca+f"/estudantes/estudante?estudante={matricula}",headers=headers)
    with open("data/student.json","w") as students_file:
        json.dump(request.json(),students_file)

#Opens file with credentials (token.json)
token_file = open("data/token.json","r")

#loads token.json
token = json.load(token_file)["token"]
print(token)

#close file dados.json
token_file.close()

#define matricula 
matricula = sys.argv[1]
print(matricula)
#get profile
print(getProfile(token))
#Salva estudante pela matricula
print(saveStudent(token,matricula))