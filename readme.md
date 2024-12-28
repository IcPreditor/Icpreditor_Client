# DCheck 

## Utilização da ferramenta

### Requisistos

Para iniciar a ferramenta é necessário python3 e acesso a internet para download dos modulos python necessários (requirements.txt)

Necessário Login SCAO para recuperar os estudantes independente do modo de recuperação.

### Arquivo de Configuração
main/configs.txt
- Exemplo

```
keep_session=true
studentsByCourse=true
periodoInicio=2020.1
periodoFim=2024.1
cursoId=14102100
```

#### Configurações

- keep_session 
    
    - true: Isso fará com que o token, caso já tenha sido gerado, seja mantido indefinidamente (data/token.json).
    Em caso de expiração do token, será necessário login.

    - false: Isso fará com que o token seja excluído após cada interação, o que significa que o login sempre será necessário.

- studentsByCourse **(Funcionalidade em desenvolvimento, mantenha'true')**
    
    - true: Os alunos serão escolhidos com base no código do curso (cursoId) e no semestre de ingresso dentro da faixa determinada (periodoInicio e periodoFim)

    - false ****: Os alunos serão escolhidos com base em suas ‘matrículas’/ID, encontradas em ‘matriculas.txt’

- periodoInicio / periodoFim
    - string que representa semestres universitários no formato: "ANO.S". S: semestre

- cursoId 
    - numero que indentifica unicamente um curso na UFCG. (8 Digits)

### Executando a Ferramenta
- cd main (Importante!!!)

- Executar script.sh dentro da pasta main.

- Aceitar instalar módulos listado (pode ser cancelado, e módulos já instalados não serão instalados novamente)

- Realizar login SCAO se necessário