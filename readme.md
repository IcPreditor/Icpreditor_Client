#ReadMe Provisório

data/credentials.json

{"credentials":{"username":"matricula","password":"senhaSCAOS#"}}

python3 genStudents.py

python3 testeRho.py


## Dados importantes:
### 1977.1 - 2023.2


## Artmap Fuzzy

Utilizando biblioteca 'python_artmap' disponibilizada no Git de David Vinicios https://github.com/DavidVinicius/python_artmap

## Organização
'data/' - .json que são lidos pelos scripts

'dataGenerator/genStudents.py' -> atualiza students.json (apartir de credentials.json)

'dataGenerator/analisarTaxas.py' -> para debug

'dataGenerator/Contador.py' -> contador para entradas discrepantes (debug)

'dataGenerator/corRacaValidation.py' -> verificar discrepancia de corPrac e corScao

'processing/processing.py' -> mapeia variváveis de students para binários

'processing/data_processing_test.py' -> teste de processing (artifact)

'teste/tabelaGenerator.py' -> apartir de parametros (rhoA e rhoB) roda o treino e teste (70% e 30%)

'teste/testeRho.py' -> roda tabelaGenerator varias vezes usando rhoA e rhoB com valores de 0.1 a 1