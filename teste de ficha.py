import tkinter as tk
import sqlite3


# Ingredientes
def cadastrar_ingrediente():
    nome_ingrediente = input("Qual o ingrediente?:")
    valor_ingrediente = float(input("Qual valor do ingrediente?:"))
    quantidade_comprada = int(input("Qual a quantidade comprada?:"))
    quant_usada = int(input("Qual quantidade utilizada?:"))
    unidade = input("Qual unidade de medida?:")
    valor_final = float(input("Qual valor final?:"))

    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute(''' Create Table If Not Exists Ingredientes(
    ID Integer Primary Key Autoincrement,
    Ingrediente Text Not Null,
    Valor_ingrediente Real,
    Quantidade Integer,
    Quant_usada Integer,
    Unidade Text Not Null,
    Valor_final Real)''')
    conexao.commit()

    cursor.execute('''Insert Into Ingredientes (
    Ingrediente,
    Valor_ingrediente,
    Quantidade,
    Quant_usada,
    Unidade,
    Valor_final) Values(?,?,?,?,?,?)''', (
    nome_ingrediente,
    valor_ingrediente,
    quantidade_comprada,
    quant_usada,
    unidade,
    valor_final))
    conexao.commit()
    print("Igrediente cadastrado")

def listar_ingrediente():
    id = int(input("ID:"))
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("Select * From Ingredientes Where id = ?", (id,)) 
    dados_ingredientes = cursor.fetchall()
    for item in dados_ingredientes:
        print(item)
def atualizar_ingrediente():
    id = int(input("Novo ID:"))
    novo_ingrediente = input("Qual novo ingrediente?:")
    novo_valor = int(input("Qual novo valor do ingrediente?:"))   
    nova_quantidade = int(input("Qual quantidade nova?:"))
    nova_unidade = input("Qual unidade nova?:")
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("Update Ingredientes Set Ingrediente = ?, Valor_ingrediente = ?, Quantidade = ?, Unidade = ? Where id = ?",(id, novo_ingrediente, novo_valor, nova_quantidade, nova_unidade,))
    conexao.commit()
    print("Ingrediente atualizado")
def excluir_ingrdiente():
    id = int(input("ID:"))
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("Delete From Ingredientes Where id = ?", (id,))
    conexao.close()
# Receitas
def cadastrar_receita():
    receita = input("Qual a receita?:")
    valor_receita = float(input("Valor da receita:"))
    quantidade = int(input("Quantidade comprada:"))
    tempo_preparo = int(input("Tempo de preparo:"))

    conexao = sqlite3.connect("ficha_tecica.db")
    cursor = conexao.cursor()
    cursor.execute('''Create Table If Not Exists Receitas(
    ID Integer Primary Key Autoincrement,
    Receita Text Not Null,
    Valor_receita Real,
    Quantidade Integer,
    Tempo_preparo Integer)''')
    conexao.commit()
    cursor.execute('''Insert Into Receitas(
    Receita,
    Valor_receita,
    Quantidade,
    Tempo_preparo) Values(?,?,?,?)''',(receita, valor_receita, quantidade, tempo_preparo))
    conexao.commit()
    conexao.close()
    print("Receita cadastrada")
def listar_receita():
    id = int(input("ID:"))
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("Select * From Receitas Where id = ?", (id,))
    dados_receitas = cursor.fetchall()
    for item in dados_receitas:
        print(item)
def atualizar_receita():
    id = int(input("Novo ID:"))
    nova_receita = input("Nova receita:")
    quantidade_nova = int(input("Nova quantidade:"))
    novo_tempo = int(input("Novo tempo de preparo:"))
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("Update Receitas Set Receita = ?, Valor_receita = ?, Quantidade = ?, Tempo_preparo = ? Where id = ?", (id, nova_receita, quantidade_nova, novo_tempo))
    conexao.commit()
    print("Receita atualizada")
def excluir_receita():
    id = int(input("ID:"))
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("Delete From Receitas Where id = ?", (id,))
    conexao.close()



janela = tk.Tk()
janela.title("Ficha técnica de Alimentos")
janela.geometry("800x600")
janela.resizable(True,False)   

frame_cadastro = tk.Frame(janela)
frame_cadastro.pack(fill="both", expand=True)

label_tabela1 = tk.Label(frame_cadastro, text="Nome do usuário:")
label_tabela1.pack(pady=3)

entry_tabela1 = tk.Entry(frame_cadastro, width=35)
entry_tabela1.pack(pady=3)

label_tabela2= tk.Label(frame_cadastro, text="Senha do usuário:")
label_tabela2.pack(pady=5)

entry_tabela2 = tk.Entry(frame_cadastro, width=35, show="*")
entry_tabela2.pack(pady=2)

button_cadastrar_ingrediente = tk.Button(janela, text="Cadastrar ingrediente", command=cadastrar_ingrediente)
button_cadastrar_ingrediente.pack(side="right", pady=5, padx=10)

button_cadastrar_receita = tk.Button(janela, text= "Cadastrar receita", command=cadastrar_receita)
button_cadastrar_receita.pack(side="right", pady=5, padx=10)
janela.mainloop()    