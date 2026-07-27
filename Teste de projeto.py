import sqlite3
conexao = sqlite3.connect('projeto.db')
cursor = conexao.cursor()

cursor.execute(
'''Create Table If Not Exists Ficha_de_alimentos (
    ID Integer Primary Key,
    Produto Text Not Null,
    Quantidade Int Integer,
    Valor_produto Real,
    Quant_usada Int Integer,
    Valor_final Real)
''')
conexao.commit()


def inserir_dados(Produto, Quantidade, Valor_produto, Quant_usada, Valor_final):
    cursor.execute(
        '''Insert Into Ficha de alimentos(Produto,Quantidade, Valor_produto, Quant_usada, Valor_final)
        Values(?,?,?,?,?)''', (Produto, Quantidade, Valor_produto, Quant_usada, Valor_final))

    conexao.commit()

Produto = input("Digite o produto:")
Quantidade = int(input("Qual quantidade do produto:"))
Valor_produto = float(input("Qual o valor do produto:"))
Quant_usada = int(input("Quatidade usada:"))
Valor_final = float(input("Qual o valor final do produto:"))
inserir_dados(Produto, Quantidade, Valor_produto, Quant_usada, Valor_final)
