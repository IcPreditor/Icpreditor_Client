#python3
#Generates .json with all students
#Uses requests to the eureca ufcg system, 
#with the credentials in credentials.json, the token is saved in token.json
#Guilherme Fernandes, 2024

import requests as req
import pandas as pd
import json

url_token = 'https://eureca.sti.ufcg.edu.br/as'
#url_token = 'https://pre.ufcg.edu.br:8443/as_scao'
#url_eureca = 'https://eureca.sti.ufcg.edu.br/das'
url_eureca= 'https://eureca.sti.ufcg.edu.br/das/v2'
#request token
def genToken(data):
    request = req.post((url_token+"/tokens"), json=data )
    #token = r.json()['token']
    #saves token in token.json
    with open("data/token.json","w") as token_file:
        json.dump(request.json(),token_file)
    #retorna token
    print(request.json())
    return request.json()["token"]

#request profile (using token)
def getProfile(token):
    headers = {'content-type':'application/json',"token-de-autenticacao":token}
    request = req.get((url_token+"/profile"),headers=headers)
    return request.json()

#request Courses Actives (using token)
def saveCoursesActives(token):
    headers = {'content-type':'application/json',"token-de-autenticacao":token}
    request = req.get(url_eureca+"/cursos?status-enum=ATIVOS&campus=1",headers=headers)
    #save coursesActives
    with open("data/coursesActives.json","w") as courses_file:
            json.dump(request.json(),courses_file)
    #return r.content

#student by course // 2017.1-2023.2
def saveStudents(token,inicio="2018.1",fim="2023.2"):
    headers = {'content-type':'application/json',"token-de-autenticacao":token}
    request = req.get(url_eureca+"/estudantes?periodo-de-evasao-de="+inicio+"&periodo-de-evasao-ate="+fim+"&situacao-do-estudante=INATIVOS&campus=1",headers=headers)
    with open("data/students.json","w") as students_file:
        json.dump(request.json(),students_file)

#Opens file with credentials (credentials.json)
credentials = open("data/credentials.json","r")

#loads .json
data = json.load(credentials)

#request token 
token = genToken(data)

#close file dados.json
credentials.close()

#get profile
print(getProfile(token))
#get courses
#print(saveCoursesActives(token))
#get students 2017
print(saveStudents(token))