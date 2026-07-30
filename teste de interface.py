import tkinter as tk
import sqlite3
janela = tk.Tk()
janela.title("Olá, Pedro Victor")
janela.geometry("800x660")
janela.resizable(True,False)
label_nome = tk.Label(janela, text= "Digite seu nome:")
label_nome.pack()
entry_nome = tk.Entry(janela)
entry_nome.pack()
label_idade = tk.Label(janela, text= "Digite sua idade:")
label_idade.pack()
entry_idade = tk.Entry(janela)
entry_idade.pack()
label_curso = tk.Label(janela, text= "Digite seu cruso:")
label_curso.pack()
entry_curso = tk.Entry(janela)
entry_curso.pack()
def exibir_nome():
    nome = entry_nome.get()
    idade = int(entry_idade.get())
    curso = entry_curso.get()

    conexao = sqlite3.connect("ficha.db")
    cursor = conexao.cursor()
    cursor.execute('''Create Table If Not Exists alunos(
    ID Integer Primary Key Autoincrement,
    Nome Text Not Null,
    Idade Integer,
    Curso Text Not Null)''')
    conexao.commit()

    cursor.execute('''Insert Into alunos (nome,idade,curso) Values(?,?,?)''',(nome,idade,curso))
    conexao.commit()

    button = tk.Button(janela,text= "Enviar", command=exibir_nome)
    button.pack()
    
janela.mainloop()

