#Test values of rhoARTa and rhoARTb
import numpy as np
from python_artmap import ARTMAPFUZZY
import bancoFalso as bf
import sys

sys.path.insert(1, r'C:\Users\m5253\VisualStudio\Icpreditor\processing')
import processing

students_in,students_out = processing.getInputOutput()
students_in = [list(item[0]) for item in students_in]
i = len(students_in)

##Training Data
input = np.array(students_in[0:i//2])
input = input.astype(int)
output = np.array(students_out[0:i//2])

##Testing Data
teste_in = np.array(students_in[i//2:i-1])
teste_in = teste_in.astype(int)
teste_out = np.array(students_out[i//2:i-1])

if output[0][0]==0:
    aux3 = [0,1]
else:
    aux3 = [1,0]

for rb_int in range(1,10,2):
    rb = rb_int/10.0
    for ra_int in range(1,10,2):
        ra = ra_int/10.0

        print("##Iniciando Treinamento##")
        print("RhoA: " + str(ra))
        print("RhoB: " + str(rb))
        ArtMap = ARTMAPFUZZY(input, output, rhoARTa=ra, rhoARTb=rb)
        ArtMap.train()
        print("##Treinamento Finalizado##")

        n = len(teste_in)
        sucesso = 0

        print("##Iniciando Teste##")
        for y in range(n):
            resultado = ArtMap.test(teste_in[y]).get("index")
            if (teste_out[y]==aux3[resultado]):
                sucesso += 1

        print("##Teste Finalizado##")
        print("Resultados:")
        print(str(sucesso)+"/"+str(n))
        print(sucesso/n)