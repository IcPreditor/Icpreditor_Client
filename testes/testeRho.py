import numpy as np
from random import choices,randint,seed
from python_artmap import ARTMAPFUZZY
import bancoFalso as bf

input,output = bf.bancoFalso(2000)

if output[0][0]==0:
    print(output[0][0])
    print(0)
    aux3 = [0,1]
else:
    print(output[0][0])
    print(1)
    aux3 = [1,0]

for rb_int in range(1,10,2):
    rb = rb_int/10.0
    for ra_int in range(1,10,2):
        ra = ra_int/10.0
        ArtMap = ARTMAPFUZZY(input, output, rhoARTa=ra, rhoARTb=rb)
        ArtMap.train()

        n = len(input)

        sucesso = 0
        for y in range(len(input)):
            resultado = ArtMap.test(input[y]).get("index")
            '''
            print("")
            print("input: " + str(input[y]))
            print("output: " + str(output[y]))
            print("ArtB:" + str(resultado)) #{'index': 0, 'ArtB': [0.0, 1.0], 'id': '0010'}
            print("")
            '''

            if (output[y]==aux3[resultado]):
                sucesso += 1

        print("RhoA: " + str(ra))
        print("RhoB: " + str(rb))
        print(str(sucesso)+"/"+str(n))
        print(sucesso/n)