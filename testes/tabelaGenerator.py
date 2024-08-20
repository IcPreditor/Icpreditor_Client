#Test values of rhoARTa and rhoARTb
#Eduardo Augusto, 2024
#Guilherme Fernandes, 2024

import numpy as np
from python_artmap import ARTMAPFUZZY
import bancoFalso as bf
import sys

sys.path.insert(1, r'C:\Users\m5253\VisualStudio\Icpreditor\processing')
import processing
#All Students Data
students_in,students_out = processing.getInputOutput()
students_in = [list(item[0]) for item in students_in]
len_students = len(students_in)

##Training Data
input = np.array(students_in[0:len_students//2])
input = input.astype(int)
output = np.array(students_out[0:len_students//2])

##Testing Data
teste_in = np.array(students_in[len_students//2:len_students-1])
teste_in = teste_in.astype(int)
teste_out = np.array(students_out[len_students//2:len_students-1])

if output[0][0]==0:
    aux3 = [0,1]
else:
    aux3 = [1,0]

#rhoARTa AND rhoARTb
ra = 0.1
rb = 0.1

print("##Iniciando Treinamento##")
print("RhoA: " + str(ra))
print("RhoB: " + str(rb))
ArtMap = ARTMAPFUZZY(input, output, rhoARTa=ra, rhoARTb=rb)
ArtMap.train()
print("##Treinamento Finalizado##")

#Number of elements in the array of test
num_ele = len(teste_in)

#Variables, for statistical reasons
sample_not_evasion = 0
success_not_evasion = 0
sample_evasion = 0
success_evasion = 0

print("##Iniciando Teste##")

for y in range(num_ele):
    result = ArtMap.test(teste_in[y]).get("index")
    if(teste_out[y]==0):
        sample_not_evasion += 1 
    elif(teste_out[y]==1):
        sample_evasion += 1

    if (teste_out[y]==aux3[result]):
        if(teste_out[y]==0):
            success_not_evasion += 1 
        elif(teste_out[y]==1):
            success_evasion += 1

print("##Teste Finalizado##")
#Variables, for statistical reasons
error_evasion = sample_evasion-success_evasion
error_not_evasion = sample_not_evasion-success_not_evasion
#Variables, percentages
success_evation_per = (success_evasion/sample_evasion)*100
success_not_evation_per = (success_not_evasion/sample_not_evasion)*100
error_evasion_per = 100.0-success_evation_per
error_not_evasion_per = 100.0-success_not_evation_per
#Variables, Total
sample_total = sample_evasion + sample_not_evasion
success_total = success_evasion + success_not_evasion
success_total_per = (success_total/sample_total)*100
error_total = error_evasion + error_not_evasion
error_total_per = (error_total/sample_total)*100
print("Resultados:")
print("{0:#^8} | {1:^19} | {2:^19} | {3:^19} |"
      .format("","Evasão","Não Evasão","Total"))

print("{0:8} | {1:^8} | {2:^8} | {3:^8} | {4:^8} | {5:^8} | {6:^8} |"
      .format("","qtd","%","qtd","%","qtd","%"))

print("{0:^8} | {1:^8} | {2:^8} | {3:^8} | {4:^8} | {5:^8} | {6:^8} |"
      .format("Amostra",sample_evasion,100.0,sample_not_evasion,100.0,sample_total,100.0))

print("{0:^8} | {1:^8} | {2:^8} | {3:^8} | {4:^8} | {5:^8} | {6:^8} |".
      format("Acerto",success_evasion,success_evation_per,success_not_evasion,success_not_evation_per,success_total,success_total_per))

print("{0:^8} | {1:^8} | {2:^8} | {3:^8} | {4:^8} | {5:^8} | {6:^8} |"
      .format("Erro",error_evasion,error_evasion_per,error_not_evasion,error_not_evasion_per,error_total,error_total_per))