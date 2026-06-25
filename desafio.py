nave_combustível = float(input("O combustível da nave está com:"))
atmosfera_planeta = input("A atmosfera é respirável?:")
traje = float(input("A capacidade do traje está com:"))

if nave_combustível >=15 and (atmosfera_planeta == 'sim'or traje == 100):
    print("Iniciando protocolo de pouso")
else:
    print("Pouso abortado: risco de morte")

escolha = int(input("1 p/ ponte e 2 p/ túnel:"))
if escolha == 1:
    carro = input("carro blindado?")
    ponte = input("ponte intacta?")
    if carro == "sim" and ponte == "sim":
        print("fuga bem-sucedida")
elif escolha == 2:
    mascara = input("possuem mascara")
    cartão = input("possuem cartão")
    if mascara == "sim" and cartão == "sim":
         print("fuga bem-sucedida")
else:
    print("sem escapatória")




