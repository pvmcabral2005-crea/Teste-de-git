a = 'Verdadeiro'
b = 'Falso'
print(a and b)
print(a or b)
print(not a)

nota = float(input("Digite sua nota:"))
frequência = float(input("Digite sua frequência:"))
if nota >= 7 and frequência >= 75:
    print("Aprovado")
else:
    print("Reprovado")

idade = int(input("Qual a sua idade:"))
carteira_CNH = input("Possui carteira?:")
if idade >=18 and carteira_CNH == "Sim":
    print("Pode dirigir")
else:
    print("Não pode dirigir")

idade = int(input("Qual a idade do eleitor:"))
titulo = input("Possui título de eleitor:")
if idade >=16 and titulo == "sim":
    print("Pode votar")
else:
    print("Não pode votar")

valor_de_compra = float(input("O valor de compra é:"))
cliente_vip = input("O cliente é vip?:")
if valor_de_compra >=100 or cliente_vip == "sim":
    print("Desconto de 10%")
    print(valor_de_compra * 0.9)
else:
    print("Compra sem desconto")
    print(valor_de_compra)