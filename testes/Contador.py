import json

estadoCivil = 0
nascimento = 0
escola = 0
genero = 0
affirmativePolicy = 0

total = 0

for aluno in json.load(open("data/students.json")):
    total += 1
    if aluno["maritalStatus"]=="DESCONHECIDO":
        estadoCivil += 1
    if aluno["placeOfBirth"] == None:
        nascimento += 1
    if aluno["secondarySchoolType"] == "DESCONHECIDA":
        escola += 1
    if aluno["gender"] != "FEMININO" and aluno["gender"] != "MASCULINO":
        genero += 1
          
print("Contagem Desconhecidos: ")
print("Estado Civil: "+str(estadoCivil)+"/"+str(total))
print("Tipo de Ensino: "+str(escola)+"/"+str(total))
print("nascimento: "+str(nascimento)+"/"+str(total))
print("nascimento: "+str(genero)+"/"+str(total))