import sqlite3
import tkinter as tk
from tkinter import ttk
conexao = sqlite3.connect('ficha_técnica.db')
cursor = conexao.cursor()

cursor.execute(
    '''Create Table If Not Exists Ingredientes (
    ID Integer Primary Key Autoincrement,
    Ingrediente Text Not Null,
    Quantidade_comprada Integer,
    Valor_ingrediente Real,
    Unidade Text Not Null)
''')

cursor.execute('''
Create Table If Not Exists Receitas (
ID Integer Primary Key Autoincrement,
Receita Text Not Null,
Quantidade Integer,
Valor_receita Real,
Tempo_Preparo Integer)''')

cursor.execute('''
Create Table If Not Exists Produtos(
ID Integer Primary Key Autoincrement,
Produto Text Not Null)''')
conexao.commit()



# Ingredientes da Ficha
def cadastrar_ingredientes():
    nome_ingrediente = input("Qual ingrediente?:")
    quantidade = int(input("Quantidade comprada:"))
    valor_ingrediente = float(input("Qual valor do ingrediente?:"))
    unidade = input("Qual unidade de medida?(kg,g,litro...):")
    conexao = sqlite3.connect('ficha.db')
    cursor = conexao.cursor()
    cursor.execute("Insert Into Ingredientes (Ingrediente, Quantidade_comprada, Valor_ingrediente, Unidade) Values (?,?,?,?)", (
    nome_ingrediente, quantidade, valor_ingrediente, unidade,))

    conexao.commit()
    print("Ingrediente cadastrado")


def listar_ingredientes():
    conexao = sqlite3.connect('ficha_técnica.db')
    cursor = conexao.cursor()
    cursor.execute("Select * From Ingredientes")
    dados_ingredientes = cursor.fetchall()
    for item in dados_ingredientes:
        print(item)



def atualizar_ingredientes():
    id = int(input("Novo ID do ingrediente:"))
    nome_ingrediente = input("Novo ingrediente:")
    unidade = input("Nova unidade de medida:")
    valor_ingrediente = float(input("Novo valor do ingrediente:"))
    conexao = sqlite3.connect('ficha.db')
    cursor = conexao.cursor()
    cursor.execute("Update Ingredientes Set Ingrediente = ?, unidade = ?, valor_ingrediente = ? Where id = ?",
                   (id, nome_ingrediente, unidade, valor_ingrediente,))
    conexao.commit()
    print("Ingrediente Atualizado")


def excluir_ingredientes():
    id = int(input("ID:"))
    conexao = sqlite3.connect('ficha_técnica.db')
    cursor = conexao.cursor()
    cursor.execute("Delete From Ingredientes Where id = ? ", (id,))

    conexao.close()
# Receitas da Ficha

def cadastrar_receita():
    nome_receita = input("Qual a receita utlizada?:")
    valor_receita = float(input("Qual preço da receita?:"))
    quantidade = int(input("Qual a quantidade?:"))
    tempo_preparo = int(input("Qual o tempo de preparação?:"))
    conexao = sqlite3.connect("ficha técnica.db")
    cursor = conexao.cursor()
    cursor.execute("Insert Into Receitas (Receita, Quantidade, Valor_receita, Tempo_Preparo) Values(?,?,?,?)",(nome_receita, quantidade, valor_receita, tempo_preparo))

    conexao.commit()
    print("Receita cadastrada")


def listar_receita():
    conexao = sqlite3.connect("ficha_técnica.db")
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
    cursor.execute("Update Receitas Set Receita = ?, Quantidade = ?, Valor_receita = ?, Tempo_Preparo = ? Where ID = ? ",
    (id, nova_receita, nova_quantidade, novo_valor, novo_tempo,))
    conexao.commit()
    print("Ingrediente atualizado")


def excluir_receita():
    id = int(input("ID:"))
    conexao = sqlite3.connect("ficha_técnica.db")
    cursor = conexao.cursor()
    cursor.execute("Delete From Receitas Where ID = ?", (id,))
    conexao.close()


while True:
    print("""===FICHA TÉCNICA INGREDIENTES===
            1- Cadastrar ingrediente
            2-Listar ingrediente
            3-Atualizar ingrediente
            4-Excluir ingrediente
            5-Cadastar receita
            6-Listar receita
            7-Atualizar receita
            8-Excluir receita
            9-Cadastrar produto
            10-Listar produto
            11-Atualizar produto
            12-Excluir produto""")

    opção = input("Digite a opção escolhida:")
    if opção == "1":
        cadastrar_ingredientes()
    elif opção == "2":
        listar_ingredientes()
    elif opção == "3":
        atualizar_ingredientes()
    elif opção == "4":
        excluir_ingredientes()
    elif opção == "5":
        cadastrar_receita()
    elif opção == "6":
        listar_receita()
    elif opção == "7":
        atualizar_receita()
    elif opção == "8":
        excluir_receita()
        break
    else:
        print("Opção inválida.Tente novamente")


janela = tk.Tk()
janela.title("Ficha técnica de Alimentos")
janela.geometry("800x600")
janela.resizable(True, False)

frame_titulo = tk.Frame(janela)

label1 = tk.Label(janela, text="Ficha de ingredientes")
label1.pack(pady=5)

colunas1 = ("ID", "Ingredientes")
tabela1 = ttk.Treeview(janela, columns=colunas1, show='headings')

label2 = tk.Label(janela, text="Ficha de receitas")
label2.pack(pady=5)

colunas2 = ("ID", "Receitas")
tabela2 = ttk.Treeview(janela, columns=colunas2, show="headings")

button_cadastrar = tk.Button(
    janela, text="Cadastrar", command=cadastrar_ingredientes)
button_cadastrar.pack()

button_listar = tk.Button(janela, text="Buscar", command=listar_ingredientes)
button_listar.pack()

button_atualizar = tk.Button(
    janela, text="Atualizar", command=atualizar_ingredientes)
button_atualizar.pack()

button_excluir = tk.Button(janela, text="Excluir",
                           command=excluir_ingredientes)
button_excluir.pack()
janela.mainloop()
