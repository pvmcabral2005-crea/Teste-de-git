#lista = [10, 5, 25, 30]
#print(sum(lista))
#print(lista[1])
#lista.append(50)
#print(lista)

#nomes = ['Maria','João','Tom']
#for i in range(3):
    #nome = input("Digite o nome:")
    #nomes.append(nome)
    #print(nomes)

#numeros = [20,8,35,7,9,8,40]
#print(len(numeros))
#print(numeros[-2])
#print(numeros[4])
#numeros.extend([18,24])
#print(numeros)
#numeros.pop(1)
#print(numeros)
#print(sorted(numeros))
#print(numeros.count(8))
#nums = [12,3,6,24,45,11]
#for i in range(len(nums)):
       #if nums[i] %2 == 0:
          #nums[i] = 0
#print('números pares substiuidos por zero são: ', nums)

#numeros = []
#pares = []
#ímpares = []
#for i in range(20): 
     #numero = int(input(f"Digite o{i+1} número:"))
     #numeros.append(numero)
     #if numero %2 == 0:
          #pares.append(numero)
#else:
     #ímpares.append(numero)
     #print("lista completa:", numeros)
     #print("numeros pares:", pares)
     #print("numeros ímpares:", ímpares)

lista_convidados = ["Pedro", "Jasper", "Carter", "Bia", "Marta"]

while True:
    print("""=======Menu=======
          1-Adicionar convidado
          2-listar convidados
          3- consultar convidados
          4-Remover convidado
          5-Quantidade de convidados
          6-Editar convidado
          0-Sair """)
    opção = int(input("Digite a opção escolhida:"))
    if opção == 1:
        convidado = input("Nome do convidado:")
        lista_convidados.append(input("Digite o convidado a ser adicionado:"))
    elif opção == 2:
        lista_convidados = input("Os convidados da lista são:")
        for i in lista_convidados:
            print(lista_convidados)
            print()
            print(i)
            count = 1
            for i in lista_convidados:
                print(f"{count} - {1}")
                count+= 1

    elif opção == 3:
       convidado = input("Digite o convidado a ser consultado:")
       if convidado in lista_convidados:
           for i in lista_convidados:
               print(f"{convidado} está na lista de convidados")
       else:
        print(f"{convidado} não está na lista de convidados")
    elif opção == 4:
        convidado = input("Digite o convidado a ser removido:")
        if convidado in lista_convidados:
            for i in lista_convidados:
                lista_convidados.remove(convidado)
                print(f"{convidado} está removido da lista")
        else:
            print(f"{convidado} não está removido da lista")
    elif opção == 5:
        print(len(lista_convidados))
    elif opção == 6:
        convidado_antigo = input("Digite o convidado a ser editado:")
        if convidado_antigo in lista_convidados:
            convidado_novo = input("Digite o novo convidado editado:")
            index = lista_convidados.index(convidado_antigo)
            lista_convidados[index] = convidado_novo
            print(f"{convidado_antigo} foi atualizado com {convidado_novo}")
        else:
            print(f"{convidado_antigo} não está na lista de convidados") 
    elif opção == 0:
        print("Saindo do programa")
        break
    else:
    print("Opção inválida, Tente novamente")
  