import json
binaryTurnos = {
    "M":'00',
    "V":'01',
    "N":'10',
    "D":'11'
}

dicTurno = {}

def getTurno():
    for c in json.load(open("data/coursesActives.json", encoding='utf-8')):
        #Medicina Engenharia Elétrica Matématica
        if c['code']=="12205100" or c['code']=="21205100" or c['code']=="19107110" or c['code']=="14123100": #exceções
            dicTurno[c['code']] = '11'
        else:
            turno = binaryTurnos[c["name"][-1]]
            dicTurno[c['code']] = turno
    dicTurno[None] = "00"
#print(dicTurno)