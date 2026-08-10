import sqlite3
conexao = sqlite3.connect("ficha.db")

cursor = conexao.cursor()

cursor.execute('''
Create Table If Not Exists Receitas (
ID Integer Primary Key Autoincrement,
Receita Text Not Null,
Quantidade Integer,
Valor_receita Real,
tempo_preparo Integer )''')

def cadastrar_receita():
    nome_receita = input("Qual a receita utlizada?:")
    valor_receita = float(input("Qual preço da receita?:"))
    quantidade = int(input("Qual a quantidade?:"))
    tempo_preparo = int(input("Qual o tempo de preparação?:"))
    conexao = sqlite3.connect("ficha.db")
    cursor = conexao.cursor()
    cursor.execute("Insert Into Receitas (Receita, Quantidade, Valor_receita, tempo_preparo,) Values(?,?,?,?)", (nome_receita, valor_receita, quantidade, tempo_preparo,))

    conexao.commit()
    print("Receita cadastrada")

def listar_receita():
    conexao = sqlite3.connect("ficha.db")
    cursor = conexao.cursor()
    cursor.execute("Select * From Receitas")
    dados_receita = cursor.fetchall()
    for item in dados_receita:
        print(item)

def atualizar_receita():
    id = int(input("ID:"))
    nova_receita = input("Qual nome da receita?:")
    nova_quantidade = int(input("Qual nova quantidade?:"))
    novo_valor = float(input("Qual novo preço da receita?:"))
    novo_tempo = int(input("Novo tempo de preparo?:"))
    conexao = sqlite3.connect("ficha.db")
    cursor = conexao.cursor()
    cursor.execute("Update Receitas Set Receita = ?, Quantidade = ?, Valor_receita = ?, tempo_preparo = ? Where ID = ? ", (id, nova_receita, nova_quantidade, novo_valor, novo_tempo,))
    conexao.commit()
    print("Ingrediente atualizado")

def excluir_receita():
    id = int(input("ID:"))
    conexao = sqlite3.connect("ficha.db")
    cursor = conexao.cursor()
    cursor.execute("Delete From Receitas Where ID = ?", (id,))
    conexao.close()

while True:
    print('''==== FICHA TÉCNICA RECEITAS ====
        1-Cadastrar receita
        2-Listar receita
        3-Atualizar receita
        4-Excluir receita''')
    opção = input("Qual opção você escolhe:")

    if opção == "1":
        cadastrar_receita()
    elif opção == "2":
        listar_receita()
    elif opção == "3":
        atualizar_receita()
    elif opção == "4":
        excluir_receita()
    else:
        print("Opção inválida. Tente novamente")