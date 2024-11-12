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
    return(request.json())

#Opens file with credentials (token.json)
token_file = open("data/token.json","r")

#loads token.json
token = json.load(token_file)["token"]

with open('data/studentsPred.json','w') as studentsPred_file:
    json.dump([],studentsPred_file)

with open('data/studentsPred.json','r') as studentsPred_file:
    studentsPred = json.load(studentsPred_file)

with open('main/matriculas.txt','r') as matricula_file:
    for matricula in matricula_file:
        matricula = matricula.strip()
        studentsPred.append(saveStudent(token,matricula))

with open('data/studentsPred.json','w') as studentsPred_file:
    json.dump(studentsPred,studentsPred_file)
