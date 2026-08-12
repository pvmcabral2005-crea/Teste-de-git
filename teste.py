import json

aluno = {'nome': 'Pedro Victor', 'idade': 21, 'curso': 'Programador de sistema'}

dados_json = json.dumps(aluno)
print(dados_json)