var1 = 10
var2 = 40
print("soma:", var1 + var2)
print("subtração:", var1 - var2)
print("multiplicação:", var1 * var2)
print("divisão:", var1 / var2)
print("divisão inteira:", var1 // var2)
print("módulo:", var1 % var2)
print("exponenciação:", var1 ** var2)

nota1 = float(input("A primeira nota é:"))
nota2 = float(input("A segunda nota é:"))
media = (nota1 + nota2)
if media >= 7:
    print("Aprovado")
elif media < 7:
    print("Reprovado")
elif media == 10:
    print("Aprovado com distinção")
