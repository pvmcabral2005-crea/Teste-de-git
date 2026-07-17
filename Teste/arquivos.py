def arquivo_leitura(ler_arquivo):
    arquivo = open(ler_arquivo, "r")
    conteudo = arquivo.read()
    print("conteúdo do arquivo:")
    print(conteudo)
    arquivo.close()

def adicionar_animal(ler_arquivo,animal):
    arquivo = open(ler_arquivo, "a")
    arquivo.write("\n" + animal)
    arquivo.close()
    
ler_arquivo = "exemplo.txt"
arquivo_leitura(ler_arquivo)

animal = input("Digite o animal que quer adicionar")
adicionar_animal(ler_arquivo, animal)
print("Arquivo atualizado")
print(ler_arquivo)