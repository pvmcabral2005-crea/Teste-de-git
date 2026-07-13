#frutas = {"maçã": 3, "uva": 4, "banana": 5, "melancia": 6}
#print(frutas["maçã"])
#if "banana" in frutas:
 #print("Banana está no dicionário")
#else:
    #print("Banana não está no dicionário")

#itens = frutas.items()
#print(frutas)

#produtos = {'carro': 215.20, "computador": 76.00, "notebook": 84.20}
#print(produtos)
#produtos["TV"] = 120.10
#del produtos["computador"]
#print(produtos)
#print(produtos.keys())
#print(produtos.values())
#for fruta in frutas:
   #print(f" A {fruta} é muito boa")

#pessoa = {
    #"nome": "Pedro",
    #"idade": 21,
    #"cidade": "Fortaleza",
    #"altura": 1.71,
    #"profissão": "programador"
#}
#print(pessoa)

#print(pessoa.values())
#pessoa["altura"] = 1.73
#print(pessoa)
#pessoa["email"] = "pvmcabral2005@gmail.com"
#pessoa["telefone"] = 996380518
#print(pessoa)
#del pessoa["altura"]
#print(pessoa)

#lista_amigos = [{"nome": "Diogo", "idade": 21, "altura": 1.73}, {"nome": "João", "idade": 14, "altura": 1.69}, {"nome": "Clara", "idade": 18, "altura": 1.71}]

#for amigo in lista_amigos:
    #print(amigo["nome"], amigo["idade"], amigo["altura"])

#for amigo in lista_amigos:
    #for chave in amigo:
        #if "João" in amigo["nome"]:
            #print("João está na lista")
        #else:
            #print("João não está na lista")

#quantidade = len(lista_amigos)
#print(f"Há {quantidade} amigos na lista")

dicionario_idiomas = {
    "House": "Casa",
    "Dog" : "Cão",
    "Tree": "Árvore",
    "Speed": "Velocidade",
     "motorcycle": "moto",
     "sky": "céu"
}
def traduzir_palavras(palavra):
    if palavra in dicionario_idiomas:
        return dicionario_idiomas[palavra]
    else:
        return "Palavra não encontrada"
    
def adicionar_palavra(tradução,palavra):
     dicionario_idiomas[palavra] = tradução
     print(f"Palavra {palavra} adicionada com sucesso")
while True:
    print("Dicionário Inglês-Português")
    print("1-Buscar Tradução")
    print("2-Adicionar Palavra")
    print("3-Sair")
    opção = input("Digite a opção que desejar:")
    if opção == "1":
        palavra_buscada = input("Digite a palavra em inglês: ")
        tradução = traduzir_palavras(palavra_buscada)
        print(f"Tradução: {tradução}")
    elif opção == "2":
         palavra_nova = input("Digite a palavra em inglês:")
         nova_tradução = input(" Digite a tradução para português:")
         adicionar_palavra(palavra_nova, nova_tradução)
    elif opção == "3":
        print("Saindo do programa")
        break
    else:
        print("Opção inválida.Tente novamente")

   