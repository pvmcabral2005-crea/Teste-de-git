import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3

# Variáveis globais para armazenar os campos de texto das telas
entry_usuario = None
entry_senha = None
entry_usuario_cadastro = None
entry_senha_cadastro = None
entry_senha_confirmar = None

# Cores Padrao
COR_FUNDO = "#FFFFFF"
COR_TEXTO = "#000000"
COR_BOTAO = "#4CAF50"
COR_BOTAO_TEXTO = "#000000"
COR_BOTAO_2 = "#ffa500"


def conectar_banco():
    """Cria o banco de dados e as tabelas, caso ainda não existam."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()

    # Cada CREATE TABLE precisa ser um execute() separado.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ADMIN (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ALUNO (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PROFESSOR (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DISCIPLINA (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL
        )
    """)

    # cursor.execute("""
    #     CREATE TABLE IF NOT EXISTS TURMA (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         nome TEXT NOT NULL,
    #         curso_id INTEGER NOT NULL,
    #         aluno_id INTEGER NOT NULL,
    #         professor_id INTEGER NOT NULL,
    #         FOREIGN KEY (aluno_id) REFERENCES ALUNO(id),
    #         FOREIGN KEY (professor_id) REFERENCES PROFESSOR(id),
    #         FOREIGN KEY (curso_id) REFERENCES DISCIPLINA(id)
    #     )
    # """)

    conexao.commit()
    conexao.close()

###################### ADMINISTRADOR############################


def criar_admin_padrao():
    """Se não existir nenhum admin no banco, cria um admin padrão."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM ADMIN")
    total_admins = cursor.fetchone()[0]

    if total_admins == 0:
        cursor.execute(
            "INSERT INTO ADMIN (usuario, senha) VALUES (?, ?)",
            ("admin", "admin123"))
        conexao.commit()

    conexao.close()


def buscar_admin_banco(usuario, senha):
    """Procura um admin pelo usuário e senha. Retorna None se não achar."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT * FROM ADMIN WHERE usuario = ? AND senha = ?",
        (usuario, senha))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado


def usuario_existe(usuario):
    """Verifica se já existe um admin cadastrado com esse usuário."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM ADMIN WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado is not None


def salvar_admin_banco(usuario, senha):
    """Insere um novo admin no banco."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO ADMIN (usuario, senha) VALUES (?, ?)", (usuario, senha))
    conexao.commit()
    conexao.close()


def atualizar_admin_banco(id_admin, usuario, senha):
    """Atualiza usuário/senha de um admin já existente."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE ADMIN SET usuario = ?, senha = ? WHERE id = ?",
        (usuario, senha, id_admin))
    conexao.commit()
    conexao.close()


def deletar_admin_banco(id_admin):
    """Remove um admin do banco pelo id."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM ADMIN WHERE id = ?", (id_admin,))
    conexao.commit()
    conexao.close()

###################### ADMINISTRADOR############################

###################### ALUNO############################


def buscar_aluno_banco():
    """Retorna todos os alunos cadastrados no banco."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM ALUNO")
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


def salvar_aluno_banco(nome, email):
    """Insere um novo aluno no banco."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO ALUNO (nome, email) VALUES (?, ?)", (nome, email))
    conexao.commit()
    conexao.close()


def atualizar_aluno_banco(id_aluno, nome, email):
    """Atualiza os dados de um aluno já existente."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE ALUNO SET nome = ?, email = ? WHERE id = ?",
        (nome, email, id_aluno))
    conexao.commit()
    conexao.close()


def deletar_aluno_banco(id_aluno):
    """Remove um aluno do banco pelo id."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM ALUNO WHERE id = ?", (id_aluno,))
    conexao.commit()
    conexao.close()

###################### ALUNO############################

###################### PROFESSOR############################


def buscar_professor_banco():
    """Retorna todos os professores cadastrados no banco."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM PROFESSOR")
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


def salvar_professor_banco(nome, email):
    """Insere um novo professor no banco."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO PROFESSOR (nome, email) VALUES (?, ?)", (nome, email))
    conexao.commit()
    conexao.close()


def atualizar_professor_banco(id_professor, nome, email):
    """Atualiza os dados de um professor já existente."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE PROFESSOR SET nome = ?, email = ? WHERE id = ?",
        (nome, email, id_professor))
    conexao.commit()
    conexao.close()


def deletar_professor_banco(id_professor):
    """Remove um professor do banco pelo id."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM PROFESSOR WHERE id = ?", (id_professor,))
    conexao.commit()
    conexao.close()

###################### PROFESSOR############################

###################### DISCIPLINA############################


def buscar_disciplina_banco():
    """Retorna todas as disciplinas cadastradas no banco."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM DISCIPLINA")
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


def salvar_disciplina_banco(nome, descricao):
    """Insere uma nova disciplina no banco."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO DISCIPLINA (nome, descricao) VALUES (?, ?)", (nome, descricao))
    conexao.commit()
    conexao.close()


def atualizar_disciplina_banco(id_disciplina, nome, descricao):
    """Atualiza os dados de uma disciplina já existente."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE DISCIPLINA SET nome = ?, descricao = ? WHERE id = ?",
        (nome, descricao, id_disciplina))
    conexao.commit()
    conexao.close()


def deletar_disciplina_banco(id_disciplina):
    """Remove uma disciplina do banco pelo id."""
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM DISCIPLINA WHERE id = ?", (id_disciplina,))
    conexao.commit()
    conexao.close()

###################### DISCIPLINA############################


################# INTERFACE GRÁFICA ####################
def limpar_janela():
    # Procura todos os widgets/frames dentro da janela e os destrói
    for widget in janela.winfo_children():
        widget.destroy()


def fazer_login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()

    if buscar_admin_banco(usuario, senha) is not None:
        messagebox.showinfo("Login", "Login bem-sucedido!")
    else:
        messagebox.showerror("Login", "Usuário ou senha incorretos.")


def fazer_cadastro():
    usuario_novo = entry_usuario_cadastro.get()
    senha_nova = entry_senha_cadastro.get()
    confirmacao = entry_senha_confirmar.get()

    # Validação 1: Campos vazios
    if not usuario_novo or not senha_nova:
        messagebox.showwarning(
            "Cadastro", "Todos os campos devem ser preenchidos!")
        return

    # Validação 2: Verificar se as senhas batem
    if senha_nova != confirmacao:
        messagebox.showerror("Cadastro", "As senhas não coincidem!")
        return

    # Validação 3: Verificar se o usuário já existe
    if usuario_existe(usuario_novo):
        messagebox.showerror("Cadastro", "Esse usuário já existe!")
        return

    # Se passou nas validações, salva o novo admin no banco
    salvar_admin_banco(usuario_novo, senha_nova)

    messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
    tela_login()


def tela_cadastro():
    # Informa ao Python que vamos modificar as variáveis globais nesta tela
    global entry_usuario_cadastro, entry_senha_cadastro, entry_senha_confirmar

    limpar_janela()
    janela.title("Cadastro")
    janela.geometry("300x350")

    # frame para a tela de cadastro
    frame_cadastro = tk.Frame(janela)
    frame_cadastro.pack(fill="both", expand=True)

    # Titulo da tela de cadastro
    label_titulo = tk.Label(
        frame_cadastro, text="Cadastro de Usuário", font=("Arial", 16))
    label_titulo.pack(pady=10)

    # Texto indicando que se deve inserir o usuario
    label_usuario = tk.Label(frame_cadastro, text="Usuário:")
    label_usuario.pack(pady=5)

    # Campo de entrada para usuario
    entry_usuario_cadastro = tk.Entry(frame_cadastro)
    entry_usuario_cadastro.pack(pady=5)

    # Texto indicando que se deve inserir a senha
    label_senha = tk.Label(frame_cadastro, text="Senha:")
    label_senha.pack(pady=5)

    # Campo de entrada para senha
    entry_senha_cadastro = tk.Entry(frame_cadastro, show="*")
    entry_senha_cadastro.pack(pady=5)

    # Texto indicando que se deve inserir a senha
    label_senha_confirmar = tk.Label(frame_cadastro, text="Confirmar Senha:")
    label_senha_confirmar.pack(pady=5)

    # Campo de entrada para senha
    entry_senha_confirmar = tk.Entry(frame_cadastro, show="*")
    entry_senha_confirmar.pack(pady=5)

    # criando botoes para fazer login e cadastrar
    frame_botoes = tk.Frame(frame_cadastro)
    frame_botoes.pack(pady=10)

    botao_cadastrar = tk.Button(frame_botoes, text="Cadastrar",
                                command=fazer_cadastro, bg=COR_BOTAO, fg=COR_BOTAO_TEXTO)
    botao_cadastrar.pack(side="left", pady=5, padx=10)

    botao_voltar = tk.Button(frame_botoes, text="Voltar",
                             command=tela_login, bg=COR_BOTAO_2, fg=COR_BOTAO_TEXTO)
    botao_voltar.pack(side="right", pady=5, padx=10)


def tela_login():
    global entry_usuario, entry_senha

    limpar_janela()
    janela.title("Login")
    janela.geometry("300x250")

    # frame para a tela de login
    frame_login = tk.Frame(janela)
    frame_login.pack(fill="both", expand=True)

    # Titulo da tela de login
    label_titulo = tk.Label(
        frame_login, text="Sistema de Login", font=("Arial", 16))
    label_titulo.pack(pady=10)

    # Texto indicando que se deve inserir o usuario
    label_usuario = tk.Label(frame_login, text="Usuário:")
    label_usuario.pack(pady=5)

    # Campo de entrada para usuario
    entry_usuario = tk.Entry(frame_login)
    entry_usuario.pack(pady=5)

    # Texto indicando que se deve inserir a senha
    label_senha = tk.Label(frame_login, text="Senha:")
    label_senha.pack(pady=5)

    # Campo de entrada para senha
    entry_senha = tk.Entry(frame_login, show="*")
    entry_senha.pack(pady=5)

    # criando botoes para fazer login e cadastrar
    frame_botoes = tk.Frame(frame_login)
    frame_botoes.pack(pady=10)

    botao_login = tk.Button(frame_botoes, text="Login",
                            command=fazer_login, bg=COR_BOTAO, fg=COR_BOTAO_TEXTO)
    botao_login.pack(side="left", pady=5, padx=10)

    botao_cadastrar = tk.Button(frame_botoes, text="Cadastrar Admin",
                                command=tela_cadastro, bg=COR_BOTAO_2, fg=COR_BOTAO_TEXTO)
    botao_cadastrar.pack(side="right", pady=5, padx=10)


# Prepara o banco de dados antes de abrir a janela
conectar_banco()
criar_admin_padrao()

# Criar janela principal
janela = tk.Tk()
janela.title("Login")
janela.geometry("300x250")
janela.resizable(False, False)
tela_login()
janela.mainloop()
