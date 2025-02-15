import sys
import requests as req
import json

url_token = 'https://eureca.sti.ufcg.edu.br/as'


#Get profile, for token test
def getProfile(token):
    headers = {'content-type':'application/json',"token-de-autenticacao":token}
    request = req.get((url_token+"/profile"),headers=headers)
    return request.status_code

def genToken(data):
    request = req.post((url_token+"/tokens"), json=data )
    #token = r.json()['token']
    #saves token in token.json
    with open("../data/token.json","w") as token_file:
        json.dump(request.json(),token_file)
    #retorna token
    print(request.status_code)
    if(request.status_code != 201 and request.status_code != 200):
        print("error token não retornado")
        return
    print("ok")
    return request.json()["token"]
if (len(sys.argv)>1):
    #Opens file with credentials (token.json)
    token_file = open("../data/token.json","r")
    #loads token.json
    token = json.load(token_file)["token"]
    status = getProfile(token)

    if(status != 200 and status != 201):
        print("ok")
    else:
        print("error token invalido")
else:
    #Opens file with credentials (credentials.json)
    credentials = open("../data/credentials.json","r")

    #loads .json
    data = json.load(credentials)
    #request token 
    token = genToken(data)

    #close file dados.json
    credentials.close()