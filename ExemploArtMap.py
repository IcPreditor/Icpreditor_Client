import numpy as np
from python_artmap import ARTMAPFUZZY
from random import choices

#gerador banco fictício 
print(choices(range(2),k=10))

input  = np.array([
        [1, 1],
        [1, 0],
        [0, 1],
        [0, 0]
])

# categoria 1 index 0
# categoria 0 index 1
output  = np.array([
        [1], # categoria 0
        [0], # categoria 1
        [0],
        [0],
])
# lista de categorias [1,0]

ArtMap = ARTMAPFUZZY(input, output, rhoARTa=0.9, rhoARTb=0.9)
ArtMap.train()

# art [chance de ser 1, chance de ser 0]
# Resutlado 0
# ArtB[0]
# ArtB[0] = 0.0 false
# ArtB[1] = 1.0 true

print(ArtMap.test([1,1])) 
print(ArtMap.test([1,0])) 
print(ArtMap.test([0,1]))
print(ArtMap.test([0,0])) 
#{'index': 0, 'ArtB': [1.0, 0.0], 'id': '1000'}
#{'index': 1, 'ArtB': [0.0, 1.0], 'id': '0010'}
#{'index': 1, 'ArtB': [0.0, 1.0], 'id': '0010'}
#{'index': 1, 'ArtB': [0.0, 1.0], 'id': '0010'}
