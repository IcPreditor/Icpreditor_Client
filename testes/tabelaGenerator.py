#Test values of rhoARTa and rhoARTb
#Eduardo Augusto, 2024
#Guilherme Fernandes, 2024

import numpy as np
from python_artmap import ARTMAPFUZZY
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import sys

sys.path.insert(1, r'processing')
import processing
#All Students Data
input,output,teste_in,teste_out,dataFrame,variaveis = processing.getInputOutput(undersampling=False,regressao=False)

print("sample : "+str(len(output)+len(teste_out)))
print("training : "+str(len(output)))
print("testing : "+str(len(teste_out)))

input = np.array(input)
output = np.array(output)
teste_in = np.array(teste_in)
teste_out = np.array(teste_out)

input = input.astype(int)
output = output.astype(int)
teste_in = teste_in.astype(int)
teste_out = teste_out.astype(int)

if output[0][0]==0:
    aux3 = [0,1]
else:
    aux3 = [1,0]

#rhoARTa AND rhoARTb
def treinamento_teste(ra,rb):
    #rhoARTa: float = 0.5,
    #rhoARTb: float = 0.5,
    #alphaARTa: float = 0.001,
    #betaARTa: int = 1,
    #alphaARTb: float = 0.001,
    #betaARTb: int = 1,
    #maxValueArta: int = 1,
    #maxValueArtb: int = 1,
    #epsilon: float = 0.001
    print("##Iniciando Treinamento##")
    print("RhoA: " + str(ra))
    print("RhoB: " + str(rb))
    print("## Variáveis")
    for v in variaveis:
        print(f" - {v}")
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
    success_evasion_per = (success_evasion/sample_evasion)*100
    success_not_evasion_per = (success_not_evasion/sample_not_evasion)*100
    error_evasion_per = 100.0-success_evasion_per
    error_not_evasion_per = 100.0-success_not_evasion_per

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

    print("{0:^8} | {1:^8} | {2:^8.1f} | {3:^8} | {4:^8.1f} | {5:^8} | {6:^8.1f} |"
        .format("Amostra",sample_evasion,100.0,sample_not_evasion,100.0,sample_total,100.0))

    print("{0:^8} | {1:^8} | {2:^8.1f} | {3:^8} | {4:^8.1f} | {5:^8} | {6:^8.1f} |".
        format("Acerto",success_evasion,success_evasion_per,success_not_evasion,success_not_evasion_per,success_total,success_total_per))

    print("{0:^8} | {1:^8} | {2:^8.1f} | {3:^8} | {4:^8.1f} | {5:^8} | {6:^8.1f} |"
        .format("Erro",error_evasion,error_evasion_per,error_not_evasion,error_not_evasion_per,error_total,error_total_per))
    success = [success_evasion_per,success_not_evasion_per]
    error = [error_evasion_per,error_not_evasion_per]

    y = ["Evasão","Não_Evasão"]
    barWidth = 0.3
    r1 = np.arange(len(success))
    r2 = [aux + barWidth for aux in r1]

    plt.figure(figsize=(10,5))
    plt.bar(r1,success,color="red",width=barWidth,label='Success')
    plt.bar(r2,error,color="blue",width=barWidth,label='Error')

    plt.ylabel("Taxa (%)")
    plt.xlabel("Evasão / Não Evasão")
    plt.title("Taxas de Sucesso e Erro previsão de Evasão")
    plt.legend()
    plt.show()