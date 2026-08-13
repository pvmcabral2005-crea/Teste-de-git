import sqlite3
import tkinter as tk
import tkinter.messagebox as messagebox                         # mensgens de aviso
from tkinter import ttk                                         # importar subbliboteca do tkinter para tabela


# variáveis globais
entry_busca_ingrediente = None

def conectar_banco_dados():
    # conexão com banco de dados
    conexao = sqlite3.connect('ficha_tecnica.db')
    cursor = conexao.cursor()

    # cria tabela ficha técnica
    cursor.execute('''CREATE TABLE IF NOT EXISTS fichas(
            id INTEGER PRIMARY KEY,
            ingrediente TEXT NOT NULL,
            quantidade_comprada INTEGER,
            valor_comprado REAL,
            quantidade_usada INTEGER,
            unidade_medida TEXT,
            valor_gasto REAL)
            ''')

    # cria tabela ingredientes
    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredientes(
            id INTEGER PRIMARY KEY,
            ingrediente TEXT NOT NULL)
            ''')

    conexao.commit()
    conexao.close()

##########################  FUNÇÕES DE INGREDIENTES    ##########################

def pesquisar_ingrediente():

    ingrediente_procurado = entry_busca_ingrediente.get().strip()

    if not ingrediente_procurado:
        messagebox.showwarning("Aviso", "O campo não pode ficar vazio!")

    else:

        conexao = sqlite3.connect("ficha_tecnica.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT id, ingrediente FROM ingredientes WHERE ingrediente LIKE ?", ("%" + ingrediente_procurado + "%",),)
        resultado = cursor.fetchall()
        conexao.close()

        # Se a pesquisa não retornar nada, você também pode avisar o usuário se quiser
        if not resultado:
            messagebox.showinfo("Informação", "Nenhum ingrediente encontrado com esse termo.")

        limpar_tabela_ingredientes()


        # Insere os resultados na tabela do Tkinter
        for linha in resultado:
            tabela_ingredientes.insert("", tk.END, values=linha)

#atualizar ingrediente
def atualizar_ingrediente(ingrediente):
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("UPDATE ingredientes SET ingrediente = ?", (ingrediente))
    conexao.commit()
    conexao.close()

#deletar ingrediente
def deletar_ingrediente(ingrediente):
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM ingredientes WHERE ingrediente = ?", (ingrediente))
    conexao.commit()
    conexao.close()

# limpar janela
def limpar_janela():
      for widget in janela.winfo_children():
            widget.destroy()

# limpa a tabela ingredientes
def limpar_tabela_ingredientes():
    
    for item in tabela_ingredientes.get_children():
        tabela_ingredientes.delete(item)

# atualiza a tabela ingredientes
def atualizar_tabela_ingredientes():

    limpar_tabela_ingredientes()

    # Conecta ao banco de dados SQLite
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, ingrediente FROM ingredientes")
    linhas = cursor.fetchall()

    # Insere os dados na Treeview
    for linha in linhas:
        tabela_ingredientes.insert("", "end", values=linha)

    conexao.close()

# deleta ingrediente da tabela ingrendientes
def deletar_ingrediente():
    selecionados = tabela_ingredientes.selection()
    
    if not selecionados:
        messagebox.showwarning("Aviso", "Selecione uma linha para deletar.")
        return
    
    # 1. Caixa de confirmação antes de alterar o banco de dados
    confirmacao = messagebox.askyesno(
        "Confirmar Exclusão", 
        f"Tem certeza que deseja deletar {len(selecionados)} item(ns)?"
    )
    
    # 2. Se o usuário clicar em "Não", interrompe a função
    if not confirmacao:
        return
        
    # 3. Se clicou em "Sim", o código abaixo continua e deleta
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    
    for item in selecionados:
        valores = tabela_ingredientes.item(item, "values")
        id_registro = valores[0]
        
        cursor.execute("DELETE FROM ingredientes WHERE id = ?", (id_registro,))
        tabela_ingredientes.delete(item)
        
    conexao.commit()
    conexao.close()
    messagebox.showinfo("Sucesso", "Registro(s) deletado(s) com sucesso!")

# abre pop-up adicionar ingrediente
def abrir_popup_adicionar_ingrediente():
    popup_adicionar_ingrediente = tk.Toplevel()
    popup_adicionar_ingrediente.title("Editar Ingrediente")
    popup_adicionar_ingrediente.geometry("300x150")
    # Bloqueia a janela principal até fechar o pop-up
    popup_adicionar_ingrediente.grab_set()

    # Elementos visuais do Pop-up
    label = tk.Label(popup_adicionar_ingrediente, text="Nome do Ingrediente:")
    label.pack(pady=10)

    entry_adicionar_ingrediente = tk.Entry(popup_adicionar_ingrediente, width=30)
    entry_adicionar_ingrediente.pack(pady=5)

    def cadastrar_ingrediente_banco():
        novo_ingrediente = entry_adicionar_ingrediente.get().strip()

        if not novo_ingrediente:
            messagebox.showwarning("Aviso", "O campo não pode ficar vazio!")
            return
        
        else:
            # Atualiza no Banco de Dados SQLite3
            conexao = sqlite3.connect("ficha_tecnica.db")
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO ingredientes (ingrediente) VALUES (?)", (novo_ingrediente,))
            conexao.commit()
            conexao.close()    

            # Atualiza a linha visualmente na tabela Tkinter
            atualizar_tabela_ingredientes()

            # Fecha o pop-up e avisa o usuário
            popup_adicionar_ingrediente.destroy()
            messagebox.showinfo("Sucesso", "Ingrediente adicionado com sucesso.")

    # Botão Salvar dentro do Pop-up
    botao_salvar = tk.Button(popup_adicionar_ingrediente, text="Salvar", command=cadastrar_ingrediente_banco)
    botao_salvar.pack(pady=15)

# abre popup para edição do nome do ingrediente    
def abrir_popup_editar_ingrediente():
    # 1. Verifica se há uma linha selecionada
    selecao = tabela_ingredientes.selection()
    if not selecao:
        messagebox.showwarning("Aviso", "Por favor, selecione um ingrediente para editar!")
        return

    # 2. Captura a linha selecionada e seus dados
    item_id = selecao[0]
    valores = tabela_ingredientes.item(item_id, "values")

    # Supondo que a tabela tem: Coluna 0 (ID) e Coluna 1 (Nome)
    id_ingrediente = valores[0]
    nome_atual = valores[1]

    # 3. Criação do pop-up editar ingrediente
    popup_editar_ingrediente = tk.Toplevel()
    popup_editar_ingrediente.title("Editar Ingrediente")
    popup_editar_ingrediente.geometry("300x150")
    # Bloqueia a janela principal até fechar o pop-up
    popup_editar_ingrediente.grab_set()

    # Elementos visuais do Pop-up
    label = tk.Label(popup_editar_ingrediente, text="Nome do ingrediente:")
    label.pack(pady=10)

    entry_editar_ingrediente = tk.Entry(popup_editar_ingrediente, width=30)
    entry_editar_ingrediente.pack(pady=5)
    # Preenche o campo com o nome atual do ingrediente
    entry_editar_ingrediente.insert(0, nome_atual)

    def atualizar_ingrediente_banco():
        # 4. Função interna para salvar os dados
        novo_nome = entry_editar_ingrediente.get().strip()

        if not novo_nome:
            messagebox.showwarning("Aviso", "O nome não pode ficar vazio!")
            return

        else:
            # Atualiza no Banco de Dados SQLite3
            conexao = sqlite3.connect("ficha_tecnica.db")
            cursor = conexao.cursor()
            cursor.execute("UPDATE ingredientes SET ingrediente = ? WHERE id = ?", (novo_nome, id_ingrediente))
            conexao.commit()
            conexao.close()

            # Atualiza a linha visualmente na tabela Tkinter
            tabela_ingredientes.item(item_id, values=(id_ingrediente, novo_nome))

            # Fecha o pop-up e avisa o usuário
            popup_editar_ingrediente.destroy()
            messagebox.showinfo("Sucesso", "Ingrediente atualizado com sucesso!")

    # Botão Salvar dentro do Pop-up
    botao_salvar = tk.Button(popup_editar_ingrediente, text="Salvar", command=atualizar_ingrediente_banco)
    botao_salvar.pack(pady=15)

##########################   TELAS   ##########################

# tela ingredientes
def tela_ingredientes():

    global entry_busca_ingrediente, tabela_ingredientes

    limpar_janela()

    # frame da tela ingredientes
    frame_ingredientes = tk.Frame(janela, borderwidth=1, relief="raised", bg="#FDC180")
    frame_ingredientes.pack(fill="both", expand=True)

    # título da tela ingredientes
    label_titulo = tk.Label(frame_ingredientes, text=" 🍴 Ingredientes 👨‍🍳", font=("Arial", 24), bg="#FDC180")
    label_titulo.pack(pady=10)

    frame_menu_ingredientes = tk.Frame(frame_ingredientes, borderwidth=1, relief="raised")
    frame_menu_ingredientes.pack(pady=10)

    # campo de busca de ingrdiente   
    entry_busca_ingrediente = tk.Entry(frame_menu_ingredientes)
    entry_busca_ingrediente.pack(side="left", padx=10, pady=5)

    # botões da tela ingredientes
    botao_ficha = tk.Button(frame_menu_ingredientes, text="Ficha Técnica", command=tela_ficha)
    botao_ficha.pack(side="right", padx=10, pady=5)
    
    botao_deletar_ingrediente = tk.Button(frame_menu_ingredientes, text="Deletar", command=deletar_ingrediente)
    botao_deletar_ingrediente.pack(side="right", padx=10, pady=5)

    botao_editar_ingrediente = tk.Button(frame_menu_ingredientes, text="Editar", command=abrir_popup_editar_ingrediente)
    botao_editar_ingrediente.pack(side="right", padx=10, pady=5)

    botao_atualizar_tabela_ingredientes = tk.Button(frame_menu_ingredientes, text="Atualizar Lista", command=atualizar_tabela_ingredientes)
    botao_atualizar_tabela_ingredientes.pack(side="right", padx=10, pady=5) 

    botao_cadastrar_ingrediente = tk.Button(frame_menu_ingredientes, text="Adicionar", command=abrir_popup_adicionar_ingrediente)
    botao_cadastrar_ingrediente.pack(side="right", padx=10, pady=5)

    botao_pesquisar_ingrediente = tk.Button(frame_menu_ingredientes, text="Pesquisar", command=pesquisar_ingrediente)
    botao_pesquisar_ingrediente.pack(side="right", padx=10, pady=5)

    estilo = ttk.Style()
    estilo.theme_use("clam")
    estilo.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#004c94", foreground="#f7941d")
    estilo.configure("Treeview", rowheight=28, font=("Arial", 10))

    # cria tabela
    tabela_ingredientes = ttk.Treeview(frame_ingredientes,columns=("id", "ingrediente") , show="headings", )

    # largura das colunas
    tabela_ingredientes.column("id", width=5, anchor="w")   # Coluna 1 com 100 pixels
    tabela_ingredientes.column("ingrediente", width=250, anchor="w")    # Coluna 2 com 250 pixels

    # títulos das colunas
    tabela_ingredientes.heading("id", text="ID")
    tabela_ingredientes.heading("ingrediente", text="Ingredientes")

    # exibe a tabela
    tabela_ingredientes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM ingredientes")
    resultado = cursor.fetchall()

    for linha in resultado:
        tabela_ingredientes.insert('', tk.END, values=linha)

    # Seleciona as colunas id e ingrediente da tabela
    cursor.execute("SELECT id, ingrediente FROM ingredientes")
    conexao.close()

# tela ficha
def tela_ficha():

    limpar_janela()

    # frame da tela ficha
    frame_ficha = tk.Frame(janela, borderwidth=1, relief="raised", bg="#FDC180")
    frame_ficha.pack(fill="both", expand=True)

    # título da tela ingredientes
    label_titulo = tk.Label(frame_ficha, text=" 🍴 Ficha Técnica de Preparo 👨‍🍳", font=("Arial", 24), bg="#FDC180")
    label_titulo.pack(pady=10)

    frame_menu = tk.Frame(frame_ficha, borderwidth=1, relief="raised")
    frame_menu.pack(pady=10)

    # botões da tela ficha
    botao_ingredientes = tk.Button(frame_menu, text="Ingredientes", command=tela_ingredientes)
    botao_ingredientes.pack(side="right", padx=10, pady=5)    

##########################   INÍCIO   ##########################

conectar_banco_dados()

# cria a janela principal
janela = tk.Tk()
janela.title("Maedu")
janela.geometry("700x500")
janela.resizable(False, False)

tela_ficha()

janela.mainloop()