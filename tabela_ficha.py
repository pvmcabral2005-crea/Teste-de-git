import sqlite3

conexao = sqlite3.connect('ficha.db')
cursor = conexao.cursor()

cursor.execute('''Create Table If Not Exists Ingredientes (
                ID Integer Primary Key Autoincrement,
                Ingredientes Text Not Null,
                Quantidade_comprada Int Integer,
                    Valor_ingrediente Real,
                    Quant_usada Int Integer,
                    Unidade Text Not Null,
                    Valor_final Real)
                ''')


def cadastrar_ingrediente():
    nome_ingrediente = input("Qual ingrediente?:")
    quantidade = int(input("Quantidade comprada:"))
    valor_ingrediente = int(input("Qual valor do ingrediente?:"))
    unidade = input("Qual unidade de medida?:")
    cursor.execute("Insert Into Ingredientes (Ingredientes, Quantidade_comprada, Valor_ingrediente, Unidade) Values (?,?,?,?)", (
        nome_ingrediente, quantidade, valor_ingrediente, unidade)
    )
    conexao.commit()
    print("Ingrediente cadastrado")


def listar_ingredientes():
    cursor.execute("Select * From Ingredientes")
    dados_ingredientes = cursor.fetchall()
    for item in dados_ingredientes:
        print(item)


def atualizar_ingredientes():
    id = int(input("Novo ID do ingrediente:"))
    nome_ingrediente = input("Novo ingrediente:")
    unidade = input("Nova unidade de medida:")
    valor_ingrediente = int(input("Novo valor do ingrediente:"))
    cursor.execute("Update ingredientes Set nome_ingrediente = ?, unidade = ?, valor_ingrediente = ? Where id = ?", (id, nome_ingrediente, unidade, valor_ingrediente))
    conexao.commit()
    print("Ingrediente Atualizado")


def excluir_ingredientes():
    id = int(input("ID:"))
    cursor.execute("Delete From Ingredientes Where id = ? ", (id,))
    conexao.commit()
