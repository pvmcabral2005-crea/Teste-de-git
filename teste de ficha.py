import tkinter as tk
import sqlite3

janela = tk.Tk()
janela.title("Ficha técnica de Alimentos")
janela.geometry("800x600")
janela.resizable(True,False)
janela.configure(bg= "lightblue")


frame_cadastro = tk.Frame(janela)
frame_cadastro.pack(fill="both", expand=True)

label_tabela1 = tk.Label(janela, text="Ficha de Ingredientes")
label_tabela1.pack(pady=5)

entry_tabela1 = tk.Entry(janela, width=40)
entry_tabela1.pack(pady=5)

label_tabela2= tk.Label(janela, text="Ficha de Receitas")
label_tabela2.pack(pady=5)

entry_tabela2 = tk.Entry(janela, width=40)
entry_tabela2.pack(pady=5)



def cadastrar_ingrediente():
    nome_ingrediente = input("Qual o ingrediente?:")
    valor_ingrediente = float(input("Qual valor do ingrediente?:"))
    quantidade_comprada = int(input("Qual a quantidade comprada?:"))
    quant_usada = int(input("Qual quantidade utilizada?:"))
    unidade = input("Qual unidade de medida?:")
    valor_usado = float(input("Qual valor usado?:"))

    conexao = sqlite3.connect("ficha_técnica")
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
    Valor_ingrediente,
    Quantidade,
    Quant_usada,
    Unidade,
    Valor_final) Values(?,?,?,?,?,?,?)''', (
    nome_ingrediente,
    valor_ingrediente,
    quantidade_comprada,
    quant_usada,
    unidade,
    valor_usado,))
    button_cadastrar = tk.Button(janela, text="Cadastrar", command=cadastrar_ingrediente)
    button_cadastrar.pack(side="left", pady=5, padx=10)
    conexao.commit()

janela.mainloop()    