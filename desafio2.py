#cont = 0
#senha = input("Digite sua senha:")
#while True:
    #if senha == "pv3103":
       # print("Seja bem-vindo")
        #break
    #else:
        #cont = cont + 1
        #if cont<3:
            #print("Acesso negado, você tem:", 3 - cont, "tentativas")
            #senha = input("Tente novamente")

#numero = int(input("Digite um número inteiro positivo:"))
#while numero>=0:
    #print(numero)
    #numero = numero - 1
    #print("Fim")

import random
num_secreto = random.randint(1, 10)
print("Bem-vindo ao jogo de adivihação")
print("Estou pensando em um número entre 1 e 10. Tenta adivinhar!")
acertou = False
while not acertou:
    palpite = int(input("Digite seu palpite:"))
    if palpite< num_secreto:
        print("O número é maior, tente novamente")
    elif palpite> num_secreto:
        print("O número é menor, tente novamente")
    else:
        print("Parabéns! Acertou o número")
        acertou = True
    


