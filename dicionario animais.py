import json
dicionario_animais = {"nome": "Tigre", 
                      "espécie": "Panthera Tigris",
                      "idade": 12}

with open("animais.json", "w") as arquivo:
    json.dump(dicionario_animais, arquivo, indent = 4)

def cadastrar_animal():
    novo_animal = {}
    novo_animal["nome"] = input("Qual o nome do animal?:")
    novo_animal["espécie"] = input("Qual a espécie do animal?")
    novo_animal["idade"] = int(input("Qual a idade do animal? (em anos):"))
    dicionario_animais.append(novo_animal)
def buscar_animal(nome_animal):
    if nome_animal in dicionario_animais:
        return f"O animal {nome_animal} está no dicionário"
    else:
        return "O animal não está ná lista"


while True:    
    print( """===Dicionário de animais===
    1-Cadastrar
    2-Buscar
     3-Listar
    4-Atualizar
    5-Apagar
    0-Sair """)
   

