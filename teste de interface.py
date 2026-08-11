import tkinter as tk
import sqlite3
janela = tk.Tk()
janela.title("Cadastro de alunos")
janela.geometry("800x660")
janela.resizable(True,False)
janela.configure(bg = "White")
label_nome = tk.Label(janela, text= "Digite seu nome:")
label_nome.pack(pady=2)
entry_nome = tk.Entry(janela, width=40)
entry_nome.pack(pady=5)
label_idade = tk.Label(janela, text= "Digite sua idade:")
label_idade.pack(pady=2)
entry_idade = tk.Entry(janela, width=40)
entry_idade.pack(pady=5)
label_curso = tk.Label(janela, text= "Digite seu curso:")
label_curso.pack(pady=2)
entry_curso = tk.Entry(janela, width=40)
entry_curso.pack(pady=5)
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

    cursor.execute('''Insert Into alunos (nome,idade,curso) Values(?,?,?)''',(nome,idade,curso,))
    conexao.commit()

button = tk.Button(janela,text= "Enviar", command=exibir_nome)
button.pack(pady=5)
    
janela.mainloop()

