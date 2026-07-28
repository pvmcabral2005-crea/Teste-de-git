import sqlite3
conexao = sqlite3.connect('ficha.db')
cursor = conexao.cursor()

cursor.execute(
'''Create Table If Not Exists Ficha_técnica_ingredientes (
    ID Integer Primary Key,
    Ingrediente Text Not Null,
    Quantidade_comprada Int Integer,
    Valor_ingrediente Real,
    Quant_usada Int Integer,
    Unidade Text Not Null,
    Valor_final Real)
''')
conexao.commit()


def inserir_dados(Ingrediente, Quantidade_comprada, Valor_ingrediente, Quant_usada, Unidade, Valor_final):
    cursor.execute(
        '''Insert Into Ficha_técnica_ingredientes(Ingrediente,Quantidade_comprada, Valor_ingrediente, Quant_usada, Unidade, Valor_final)
        Values(?,?,?,?,?,?)''', (Ingrediente, Quantidade_comprada, Valor_ingrediente, Quant_usada, Unidade, Valor_final))
    conexao.commit()

Ingrediente = input("Digite o ingrediente utilizado:")
Quantidade_comprada = int(input("Qual a quantidade do produto:"))
Valor_ingrediente = float(input("Qual o valor do produto: R$ "))
Quant_usada = int(input("Quantidade usada:"))
Unidade = input("Qual unidade de medida:")
Valor_final = float(input("Qual o valor final do produto:R$ "))
inserir_dados(Ingrediente, Quantidade_comprada, Valor_ingrediente, Quant_usada, Unidade, Valor_final)

