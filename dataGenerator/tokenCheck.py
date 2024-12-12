import requests as req
import json

url_token = 'https://eureca.sti.ufcg.edu.br/as'

#Opens file with credentials (credentials.json)
credentials = open("data/credentials.json","r")

#loads .json
data = json.load(credentials)


def genToken(data):
    request = req.post((url_token+"/tokens"), json=data )
    #token = r.json()['token']
    #saves token in token.json
    with open("data/token.json","w") as token_file:
        json.dump(request.json(),token_file)
    #retorna token
    #print(request.json())
    return request.json()["token"]

#request token 
token = genToken(data)

#close file dados.json
credentials.close()