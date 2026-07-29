import sqlite3
conexao = sqlite3.connect("ficha.db")
cursor = conexao.cursor()

cursor.execute(
    '''Create Table If Not Exists Ficha_técnica_receita(
    Id Integer Primary Key Autoincrement,
    Receita Text Not Null,
    Quantidade Int,
    Valor_Receita Real,
    Quant_usada Int,
    Valor_final Real)'''
)
conexao.commit()

def inserir_dados(Receita, Quantidade, Valor_receita, Quant_usada, Valor_final):
    cursor.execute(
        '''Insert Into Ficha_técnica_receita(Receita, Quantidade, Valor_receita, Quant_usada, Valor_final)
        Values(?,?,?,?,?)''', (Receita, Quantidade, Valor_receita, Quant_usada, Valor_final))
    conexao.commit()

Receita = input("Qual receita utilizada:")
Quantidade = int(input("Qual a quantidade da receita:"))
Valor_receita = float(input("Qual o valor da receita: R$"))
Quant_usada = int(input("Qual a quantidade usada:"))
Valor_final = float(input("Qual o valor final:R$ "))

inserir_dados(Receita, Quantidade, Valor_receita, Quant_usada, Valor_final)
