import sqlite3

conexao = sqlite3.connect('Ingrediente.db')
cursor = conexao.cursor()

cursor.execute('''Create Table If Not Exists Ficha_ingredientes (
ID Integer Primary Key Autoincrement,
Ingredientes Text Not Null,
Quantidade_comprada Integer,
Valor_ingrediente Real,
 Quant_usada Int Integer,
 Unidade Text Not Null,
  Valor_final Real)
''')


def cadastrar_ingredientes():
    nome_ingrediente = input("Qual ingrediente?:")
    quantidade = int(input("Quantidade comprada:"))
    valor_ingrediente = float(input("Qual valor do ingrediente?:"))
    unidade = input("Qual unidade de medida?(kg,g,litro...):")
    cursor.execute("Insert Into Ficha_ingredientes (Ingredientes, Quantidade_comprada, Valor_ingrediente, Unidade) Values (?,?,?,?)", (
        nome_ingrediente, quantidade, valor_ingrediente, unidade,))
    
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
    valor_ingrediente = float(input("Novo valor do ingrediente:"))
    cursor.execute("Update Ficha_ingredientes Set nome_ingrediente = ?, unidade = ?, valor_ingrediente = ? Where id = ?", (id, nome_ingrediente, unidade, valor_ingrediente,))
    conexao.commit()
    print("Ingrediente Atualizado")


def excluir_ingredientes():
    id = int(input("ID:"))
    cursor.execute("Delete From Ingredientes Where id = ? ", (id,))
    conexao.commit()
while True:
    print("""===FICHA TÉCNICA DE ALIMENTOS===
            1- Cadastrar ingrediente
            2-Listar ingrediente
            3-Atualizar ingrediente
            4-Excluir ingrediente""")

    opção = input("Digite a opção escolhida:")
    if opção == "1":
        cadastrar_ingredientes()
    elif opção == "2":
        listar_ingredientes()
    elif opção == "3":
        atualizar_ingredientes()
    elif opção == "4":
        excluir_ingredientes()
        break
    else:
        print("Opção inválida.Tente novamente")
    conexao.close()