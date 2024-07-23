import requests as req
import pandas as pd
import json

url = 'https://pre.ufcg.edu.br:8443/as_scao'
url2 = 'https://eureca.sti.ufcg.edu.br/das'

#token controller / requisita token
def genToken(data):
    r = req.post((url+"/as/tokens"), json=data )
    #token = r.json()['token']
    #salva token em token.json
    with open("data/token.json","w") as file:
        json.dump(r.json(),file)
    #retorna token
    return r.json()["token"]

#profile-controller / requisita perfil refente ao token
def getProfile(token):
    headers = {'content-type':'application/json',"authentication-token":token}
    r = req.get((url+"/as/profile"),headers=headers)
    return r.json()

#Courses Actives
def saveCoursesActives(token):
    headers = {'content-type':'application/json',"authentication-token":token}
    r = req.get(url2+"/courses/getActives",headers=headers)
    #save coursesActives
    with open("data/coursesActives.json","w") as file:
            json.dump(r.json(),file)
    #return r.content

#Aluno by course // 2017.1-2023.2
def saveStudents(token):
    headers = {'content-type':'application/json',"authentication-token":token}
    students = []
    for curso in json.load(open("data/coursesActives.json")):
        r = req.get(url2+"/students?courseCode="+curso["code"]+"&from=2023.1&to=2023.2&anonymize=true",headers=headers)
        students.extend(r.json()["students"])
    with open("data/students.json","w") as file:
        json.dump(students,file)


#Abre arquivo com credenciais
cred = open("data/credentials.json","r")

#Carrega .json
data = json.load(cred)

#gera token 
token = genToken(data)

#fecha dados.json
cred.close()

#get profile
print(getProfile(token))
print("#################")
#get courses
print(saveCoursesActives(token))
#get students 2017
print(saveStudents(token))