#for i in range(1,20,2):
   # print(i)

#n = int(input('Digite o número:'))
#soma = 0
#for i in range(1,n+1):
   # soma += i
    #print(f'O valor total da soma de 1 até {n} é {soma}')

#num = int(input('Digite um número:'))
#for i in range(1,11):
    #print(f"{num} x {i} = {num*i} ")

#num = int(input('Digite um número para operação:'))
#resultado = 1

#for i in range(1,num + 1):
    # resultado *= i
    # print(f"O fatorial de {num} é {resultado}")

#num = int(input('número de contagem regressiva:'))
#for i in range(num,0,-1):
   # print(i)

#total = 0
#for num in range(1,51):
   #if num % 2 == 0:
        #total+= num
#print(total)

#for letra in "Brasil":
      # print(letra)

#frase = input('Frase escolhida:').replace(" ","")
#cont = 0
#for caractere in frase:
        # cont+= 1
        # print(f"A frase possui {cont} caracteres")

#num = 10
#val1,val2 = 0,1
#for i in range(num):
    #print(val1,end = " ")
    #val1,val2 = val2, val1 + val2

base = int(input('Digite o número da base: '))
expoente = int(input('Digite o número do expoente: '))
resultado = 1
for i in range(expoente):
    resultado *= base
    print(resultado)