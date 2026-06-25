
Ano = int(input("Digite o ano de nascimento:"))
idade = 2026 - Ano
if idade>= 16:
    print('pode votar este ano')
else:
    print('não pode votar este ano')

senha = int(input("Digite a senha do usuário:"))
if senha == 1234:
    print("Acesso Permitido")
else:
    print("Acesso Negado")

maçãs_compradas =  int(input("Quantas maçãs foram compradas:"))
if maçãs_compradas<= 12:
    valor_total = 0.30 * maçãs_compradas
    print(f"o valor da compra é R${valor_total}")
else:
    valor_total = 0.25 * maçãs_compradas
    print(f"o valor da compra é R${valor_total}") 

altura = float(input('Digite sua altura:'))
sexo = int(input("Digite 1 p/feminino ou 2 p/masculino"))
if sexo == 1:
    peso_ideal = (62.3 * altura) - 44.7
    print(f"seu peso ideal é{peso_ideal:.2f}")
else:
    peso_ideal = (70.2 * altura) - 58
    print(f"seu peso ideal é{peso_ideal:.2f}")                   