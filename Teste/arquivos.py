#def arquivo_leitura(ler_arquivo):
   # arquivo = open(ler_arquivo, "r")
    #conteudo = arquivo.read()
    #print("conteúdo do arquivo:")
    #print(conteudo)
    #arquivo.close()

#def adicionar_animal(ler_arquivo,animal):
    #arquivo = open(ler_arquivo, "a")
    #arquivo.write("\n" + animal)
    #arquivo.close()
    
#ler_arquivo = "exemplo.txt"
#arquivo_leitura(ler_arquivo)

#animal = input("Digite o animal que quer adicionar:")
#adicionar_animal(ler_arquivo, animal)
#print("Arquivo atualizado")
#print(ler_arquivo)

#def contar_vogais():
    #texto_arquivo = input("Digite o seu arquivo de texto: ")
    #vogais = "AEIOUaeiou"
    #total_vogais = 0
    #try:
        #with open(texto_arquivo, "r", encoding = "utf-8") as arquivo: 
            #conteudo = arquivo.read().lower()
            #for caractere in conteudo:
                #if caractere in vogais:
                    #total_vogais+=1
            #print(f"O arquivo de texto possui {total_vogais} vogais no texto ")
    #except:
        #print(f"O arquivo não foi encontrado. Digite o texto.")
#contar_vogais()

#def caracteres_texto():
    #texto = input("Digite o texto do arquivo com um caractere:")
    #caractere = "@"
    #total_caracteres = 0
    #try:
        #with open(texto, "r", encoding = "utf-8") as arquivo:
            #conteudo = arquivo.read()
            #for caracteres in conteudo:
                #if caracteres in caractere:
                    #total_caracteres+=1
            #print(f"O caractere {caractere} aparece {total_caracteres} vezes no texto")
   # except:
        #print("Caractere não foi encontrado. Digite o texto novamente.")
#caracteres_texto()

def substituir_vogais():
    texto = input("Digite o arquivo de texto:")
    vogais = "aeiou"
    novo_texto =[]
    try:
        with open(texto, "r", encoding = "utf-8") as arquivo:
            conteudo = arquivo.read().lower()
            for caractere in conteudo:
                if caractere in vogais:
                    novo_texto.append('*')
                else:
                    novo_texto.append(caractere)
        with open("texto_substituido.txt", "w", encoding = "utf-8") as arquivo:
            arquivo.write(novo_texto)
            print("Novo arquivo criado com sucesso!")
    except:
        print("Arquivo não encontrado.Digite novamente")
substituir_vogais()
                           