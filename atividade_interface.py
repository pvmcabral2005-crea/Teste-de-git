import tkinter as tk
import tkinter.messagebox as messagebox

nome_usuario = "Pedro admin"
senha_usuario = "Pedro3103"

entry_usuario = None
entry_senha = None
def limpar_janela():
    for widget in janela.winfo_children():
        widget.destroy()

def fazer_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if usuario == nome_usuario and senha == senha_usuario:
        messagebox.showinfo("Login", "Cadastro bem sucedido!")
    else:
        messagebox.showerror("Login", "Senha ou usuário incorretos!")

def tela_login():
    global entry_usuario, entry_senha

    limpar_janela()
    tabela2 = tk.Tk()
    tabela2.title("Login")
    tabela2.geometry("300x350")
    frame_login = tk.Frame(tabela2)
    frame_login.pack(fill="both", expand=True)
    label_titulo = tk.Label(frame_login, text="Sistema de Login", font=("Arial", 18))
    label_titulo.pack(pady=5)

    label_usuario = tk.Label(frame_login, text="Login:")
    label_usuario.pack(pady=5)

    entry_usuario = tk.Entry(frame_login)
    entry_usuario.pack(pady=5)

    label_senha = tk.Label(frame_login, text="Senha:")
    label_senha.pack(pady=10)
    entry_senha = tk.Entry(frame_login, show="*")
    entry_senha.pack(pady=10)

    frame_botoes = tk.Frame(frame_login)
    frame_botoes.pack(pady=6) 
    botao_login = tk.Button(frame_botoes, text="Login", command=fazer_login)
    botao_login.pack(side="left", pady=5, padx=10)
    botao_cadastrar = tk.Button(frame_botoes, text="Cadastrar", command=fazer_cadastro)
    botao_cadastrar.pack(side="right", pady=5, padx=10)

def fazer_cadastro():

    tabela = tk.Tk()
    tabela.title("Usuários")
    tabela.geometry("600x550")
    frame_cadastro = tk.Frame(tabela)
    frame_cadastro.pack(fill="both", expand=True)
    label_titulo = tk.Label(frame_cadastro, text="Cadastro de Usuário", font=("Arial",17))
    label_titulo.pack(pady=10)

    label_usuario = tk.Label(frame_cadastro, text="Usuário:")
    label_usuario.pack(pady=5)

    entry_usuario = tk.Entry(frame_cadastro)
    entry_usuario.pack(pack=5)

    label_senha = tk.Label(frame_cadastro, text="Senha:")
    label_senha.pack(pady=8)

    entry_senha = tk.Entry(frame_cadastro)
    entry_senha.pack(pady=8)

    label_senha_confirmar = tk.Label(frame_cadastro, text="Confirmar Senha:")
    label_senha_confirmar.pack(pady=9)

    entry_senha_confirmar = tk.Entry(frame_cadastro, show="*")
    entry_senha_confirmar.pack(pady=9)

    frame_botoes = tk.Frame(frame_cadastro)
    frame_botoes.pack(pady=10)

    button_cadastrar = tk.Button(frame_cadastro, text="Cadastrar usuário", command=fazer_cadastro)
    button_cadastrar.pack(side="left", pady=5, padx=10)

    button_voltar = tk.Button(frame_cadastro, text="Voltar", command=tela_login)
    button_voltar.pack(side="right",pady=5, padx=10 )


janela = tk.Tk()
janela.title("Sistema de Frames")
janela.geometry("700x600")
janela.resizable(True,False)
frame_login = tk.Frame(janela)
frame_login.pack(fill="both", expand=True)

label_titulo = tk.Label(janela, text= "Sistema de login", font=("Arial", 18))
label_titulo.pack(pady=8)

label_usuario = tk.Label(janela, text= "Nome de usuário:")
label_usuario.pack(pady=8)

entry_usuario = tk.Entry(janela)
entry_usuario.pack(pady=5)

label_senha = tk.Label(janela, text="Senha de usuário:")
label_senha.pack(pady=5)

entry_senha = tk.Entry(janela)
entry_senha.pack(pady=5)

button_login = tk.Button(janela, text="Login", command=fazer_login)
button_login.pack(pady=10)

janela.mainloop()
