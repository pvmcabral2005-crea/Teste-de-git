import sqlite3
import tkinter as tk
from tkinter import ttk
conexao = sqlite3.connect('ficha.db')
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
Quant_usada Integer )''')

cursor.execute('''
Create Table If Not Exists Produtos(
ID Integer Primary Key Autoincrement,
Produto Text Not Null)''')
conexao.commit()

def tabela_limpa():
    for item in tabela.get_children():
        tabela.delete(item)

def busca_tabela_dados():

    cursor.execute("Select ID, nome_ingrediente From Ingredientes")
    linha = cursor.fetchall()

    for linhas in linha:
        tabela.insert("", "end", values=linhas)
conexao.close()

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

    conexao.close()

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


janela = tk.Tk()
janela.title("Cadastro de ingredientes")
janela.geometry("800x600")
janela.resizable(True,False)

frame_titulo = tk.Frame(janela)

label = tk.Label(janela, text="Ficha técnica de ingredientes")
label.pack(pady=5)

colunas = ("ID", "Ingredientes")
tabela = ttk.Treeview(janela, columns=colunas, show= 'headings')


busca_tabela_dados()

button_cadastrar = tk.Button(janela, text="Cadastrar", command= cadastrar_ingredientes)
button_cadastrar.pack()

button_listar = tk.Button(janela, text="Buscar", command= listar_ingredientes)
button_listar.pack()

button_atualizar = tk.Button(janela, text="Atualizar", command= atualizar_ingredientes)
button_atualizar.pack()

button_excluir = tk.Button(janela, text="Excluir", command= excluir_ingredientes)
button_excluir.pack()
janela.mainloop()