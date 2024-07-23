import numpy as np
from random import choices,randint
from python_artmap import ARTMAPFUZZY

def genOutput(a):
    #print(a)
    if len(a)==1:
        return a[0]
    else:
        aux = []
        aux2 = 0
        for i in range(0,len(a),2):
            if a[i]==a[i+1]:
                aux.append(0)
            else: 
                aux.append(1)
            aux2+=1
        return genOutput(aux)
            
    
def bancoFalso(num,ele=16):
    input_aux = []
    output_aux = []
    for x in range(num):
        a = choices(range(2),k=ele)
        b = genOutput(a)
        input_aux.append(a)
        output_aux.append([b])

    #print(input_aux)
    input = np.array(input_aux)
    #print(input)
    #print(output_aux)
    output = np.array(output_aux)
    #print(output)
    
    return (input,output)

#print(genOutput(choices(range(2),k=16)))