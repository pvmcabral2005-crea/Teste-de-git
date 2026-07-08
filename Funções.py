#def nome_do_usuário():
    #nome = input("Digite o nome:")
    #print(f"Olá, meu nome é {nome} ")

#nome_do_usuário()

#def menu():
    #while True:
        #print("""Escolha uma das opções abaixo:
             #1-Soma
             #2-Subtração
             #3-Multiplicação
             #4-Divisão
             #5-Sair""")
        #opção = int(input("Digite a opção escolhida:"))
        #if opção == 1:
            #soma()
        #elif opção == 2:
            #subtração()
        #elif opção == 3:
            #multiplicação()
        #elif opção == 4:
            #divisão()
        #elif opção == 5:
            #print("Saindo do programa")
            #break
        #else:
            #print("Opção inválida.Tente novamente")

#def soma():
        #num1 = int(input("Digite primeiro número:"))
        #num2 = int(input("Digite segundo número"))
        #resposta = num1 + num2
        #print(f"O resultado é {resposta}")
#def subtração():
        #num1 = int(input("Digite primeiro número:"))
        #num2 = int(input("Digite segundo número:"))
        #resposta = num1 - num2
        #print(f"O resultado é {resposta}")

#def multiplicação():
    #num1 = int(input("Digite primeiro número:"))
    #num2 = int(input("Digite segundo número:"))
    #resposta = num1 * num2
    #print(f"O resultado é {resposta}")
#def divisão():
    #num1 = int(input("Digite primeiro número:"))
   # num2 = int(input("Digite segundo número:"))
    #if num2!= 0:
       #resposta = num1 / num2
       #print(f"O resultado é {resposta}")
    #else:
        #print("Erro: Divisão por zero não é permitida")
#menu()

def soma(a,b,c):
   return a+b+c
resultado = soma(30,50,20)
print(resultado)

def calcular_media(n1,n2):
   n1 = float(input("Digite a primeira nota:"))
   n2 = float(input("Digite a segunda nota:"))
   media = (n1 + n2)/2
   return media
resultado = calcular_media(8.0,6.2)
print(resultado)

