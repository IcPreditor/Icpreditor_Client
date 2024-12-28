import sys
import requests as req
import pandas as pd
import json

url_eureca= 'https://eureca.sti.ufcg.edu.br/das/v2'


def getCourses(curso_id):
    request = req.get(url_eureca+f'/cursos?status-enum=ATIVOS&campus=1&curso={curso_id}',headers=headers)
    return request.json()


def getStudentsByCourse(curso_id,begin,end):
    request = req.get(url_eureca+f'/estudantes?periodo-de-ingresso-de={begin}&periodo-de-ingresso-ate={end}&situacao-do-estudante=ATIVOS&campus=1&curso={curso_id}',headers=headers)
    return request.json()


#Opens file with credentials (token.json)
token_file = open("../data/token.json","r")

#loads token.json
token = json.load(token_file)["token"]
#headers
headers = {'content-type':'application/json',"token-de-autenticacao":token}

with open('../data/studentsPrediction.json','w') as studentsPred_file:
    students = getStudentsByCourse(curso_id=sys.argv[1],begin=sys.argv[2],end=sys.argv[3])
    json.dump(students,studentsPred_file)

