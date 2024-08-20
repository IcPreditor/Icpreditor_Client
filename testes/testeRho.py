#Test values of rhoARTa and rhoARTb
#Eduardo Augusto, 2024
#Guilherme Fernandes, 2024
import numpy as np
from python_artmap import ARTMAPFUZZY
import bancoFalso as bf
import sys

sys.path.insert(1, r'C:\Users\m5253\VisualStudio\Icpreditor\processing')
import processing

students_in,students_out = processing.getInputOutput()
students_in = [list(item[0]) for item in students_in]
lenStudents = len(students_in)

##Training Data
input = np.array(students_in[0:lenStudents//2])
input = input.astype(int)
output = np.array(students_out[0:lenStudents//2])

##Testing Data
teste_in = np.array(students_in[lenStudents//2:lenStudents-1])
teste_in = teste_in.astype(int)
teste_out = np.array(students_out[lenStudents//2:lenStudents-1])

if output[0][0]==0:
    aux3 = [0,1]
else:
    aux3 = [1,0]

#Testing values of RhoARTa and RhoARTb between 0.1 and 1 
for rb_int in range(1,10,2):
    rb = rb_int/10.0
    for ra_int in range(1,10,2):
        ra = ra_int/10.0
        #Training
        print("##Iniciando Treinamento##")
        print("RhoA: " + str(ra))
        print("RhoB: " + str(rb))
        ArtMap = ARTMAPFUZZY(input, output, rhoARTa=ra, rhoARTb=rb)
        ArtMap.train()
        print("##Treinamento Finalizado##")

        n = len(teste_in)
        success = 0
        #Testing
        print("##Iniciando Teste##")
        for y in range(n):
            result = ArtMap.test(teste_in[y]).get("index")
            #Verifing Success
            if (teste_out[y]==aux3[result]):
                success += 1

        print("##Teste Finalizado##")
        print("Resultados:")
        print(str(success)+"/"+str(n))
        print(success/n)