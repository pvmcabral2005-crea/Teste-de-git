import sqlite3
import tkinter as tk
import tkinter.messagebox as messagebox                         # mensagens de aviso
import tkinter.filedialog as filedialog                         # selecionar imagem
from tkinter import ttk                                         # tabela / treeview
from datetime import date

try:
    from PIL import Image, ImageTk                              # exibir/miniaturizar imagem
    PIL_OK = True
except ImportError:
    PIL_OK = False


# ==========================================================
#  PALETA DE CORES E FONTES (estilo minimalista neutro)
# ==========================================================
COR_FUNDO_PRINCIPAL   = "#FAFAFA"   # quase branco, fundo geral
COR_FUNDO_HEADER      = "#FAFAFA"   # mesmo tom do fundo, sem bloco colorido
COR_FUNDO_MENU        = "#FFFFFF"   # branco, barra de menu
COR_BORDA             = "#E4E4E4"   # cinza claro para linhas/bordas finas
COR_TEXTO_TITULO      = "#1A1A1A"   # quase preto
COR_TEXTO_ESCURO      = "#333333"   # cinza escuro, texto geral
COR_TEXTO_SUBTITULO   = "#8A8A8A"   # cinza médio
COR_BOTAO             = "#FFC504"   # preto suave
COR_BOTAO_HOVER       = "#3A3A3A"   # cinza escuro (hover)
COR_BOTAO_TEXTO       = "#FFFFFF"
COR_BOTAO_SECUNDARIO       = "#FFFFFF"  # botões neutros com contorno
COR_BOTAO_SECUNDARIO_HOVER = "#F0F0F0"
COR_BOTAO_PERIGO      = "#B3261E"   # vermelho discreto para deletar
COR_BOTAO_PERIGO_HOVER = "#8C1D17"
COR_TABELA_HEADER_BG  = "#FFFFFF"
COR_TABELA_HEADER_FG  = "#1A1A1A"
COR_TABELA_LINHA_PAR  = "#FFFFFF"
COR_TABELA_LINHA_IMPAR = "#F5F5F5"
COR_TABELA_SELECAO    = "#1A1A1A"
COR_IMAGEM_PLACEHOLDER = "#EAF4FB"
COR_ACCENT            = "#5E8B85"   # verde-azulado dos botões do print

FONTE_TITULO   = ("Segoe UI", 20, "normal")
FONTE_SUBTITULO = ("Segoe UI", 10, "normal")
FONTE_BOTAO    = ("Segoe UI", 10, "normal")
FONTE_ENTRY    = ("Segoe UI", 11)
FONTE_TABELA   = ("Segoe UI", 10)
FONTE_TABELA_HEADER = ("Segoe UI", 10, "bold")


# ==========================================================
#  ESTADO GLOBAL (referências de widgets usados entre funções)
# ==========================================================
entry_busca_ficha = None
entry_busca_ingrediente = None

frame_linhas_ingredientes = None

ficha_atual_id = None
imagem_atual_path = None
imagem_tk_ref = None
label_imagem = None

entry_preparo = None
entry_profissional = None
entry_criacao = None
entry_atualizacao = None
entry_rendimento = None
text_modo_preparo = None
tabela_insumos = None
label_total_valor = None


# ==========================================================
#  BANCO DE DADOS
# ==========================================================
def migrar_banco_dados(cursor):
    """Ajusta tabelas antigas (se existirem) para o novo formato, sem apagar dados."""

    # ingredientes: garante coluna unidade_medida
    cursor.execute("PRAGMA table_info(ingredientes)")
    colunas_ing = [c[1] for c in cursor.fetchall()]
    if colunas_ing and "unidade_medida" not in colunas_ing:
        cursor.execute("ALTER TABLE ingredientes ADD COLUMN unidade_medida TEXT")

    # fichas: se a tabela antiga não tiver as colunas novas, renomeia para não colidir
    cursor.execute("PRAGMA table_info(fichas)")
    colunas_fichas = [c[1] for c in cursor.fetchall()]
    esperado = {"id", "preparo", "profissional", "criacao", "atualizacao",
                "imagem_path", "modo_preparo", "rendimento"}
    if colunas_fichas and not esperado.issubset(set(colunas_fichas)):
        cursor.execute("ALTER TABLE fichas RENAME TO fichas_antiga")


def conectar_banco_dados():
    conexao = sqlite3.connect('ficha_tecnica.db')
    cursor = conexao.cursor()

    migrar_banco_dados(cursor)

    # tabela de ingredientes (cadastro mestre)
    cursor.execute('''CREATE TABLE IF NOT EXISTS ingredientes(
            id INTEGER PRIMARY KEY,
            ingrediente TEXT NOT NULL,
            unidade_medida TEXT)
            ''')

    # tabela de fichas técnicas
    cursor.execute('''CREATE TABLE IF NOT EXISTS fichas(
            id INTEGER PRIMARY KEY,
            preparo TEXT NOT NULL,
            profissional TEXT,
            criacao TEXT,
            atualizacao TEXT,
            imagem_path TEXT,
            modo_preparo TEXT,
            rendimento TEXT)
            ''')

    # tabela de insumos (linhas de ingredientes usados em cada ficha)
    cursor.execute('''CREATE TABLE IF NOT EXISTS insumos(
            id INTEGER PRIMARY KEY,
            ficha_id INTEGER NOT NULL,
            ingrediente TEXT NOT NULL,
            quantidade_comprada REAL,
            valor_comprado REAL,
            quantidade_usada REAL,
            unidade_medida TEXT,
            valor_gasto REAL,
            FOREIGN KEY(ficha_id) REFERENCES fichas(id))
            ''')

    conexao.commit()
    conexao.close()


##########################  BOTÃO ESTILIZADO (helper)  ##########################

def criar_botao(pai, texto, comando, cor=COR_ACCENT, cor_hover=COR_BOTAO_HOVER, texto_cor=COR_BOTAO_TEXTO):
    """Cria um botão flat (formato 'pill') com efeito hover."""
    botao = tk.Button(
        pai,
        text=texto,
        command=comando,
        font=FONTE_BOTAO,
        bg=cor,
        fg=texto_cor,
        activebackground=cor_hover,
        activeforeground=texto_cor,
        relief="flat",
        bd=0,
        padx=14,
        pady=6,
        cursor="hand2",
        highlightthickness=0,
    )
    botao.bind("<Enter>", lambda e: botao.config(bg=cor_hover))
    botao.bind("<Leave>", lambda e: botao.config(bg=cor))
    return botao


def criar_botao_secundario(pai, texto, comando):
    """Botão neutro com contorno fino, para ações menos críticas."""
    botao = criar_botao(
        pai, texto, comando,
        cor=COR_BOTAO_SECUNDARIO,
        cor_hover=COR_BOTAO_SECUNDARIO_HOVER,
        texto_cor=COR_TEXTO_ESCURO,
    )
    botao.config(highlightthickness=1, highlightbackground=COR_BORDA, highlightcolor=COR_BORDA)
    return botao


def criar_botao_icone(pai, simbolo, comando, cor):
    """Botão para ações na tabela (Editar / Excluir)."""
    botao = tk.Button(
        pai, 
        text=simbolo, 
        command=comando,
        font=("Segoe UI", 9, "bold"), 
        bg=cor, 
        fg="#FFFFFF",
        relief="flat", 
        bd=0, 
        padx=8,         
        pady=2, 
        cursor="hand2", 
        highlightthickness=0,
    )
    return botao


def limpar_janela():
    for widget in janela.winfo_children():
        widget.destroy()


def criar_header(pai, titulo):
    """Cabeçalho minimalista: título + linha fina de separação (igual em todas as telas)."""
    header = tk.Frame(pai, bg=COR_FUNDO_HEADER)
    header.pack(fill="x")

    label_titulo = tk.Label(header, text=titulo, font=FONTE_TITULO, bg=COR_FUNDO_HEADER, fg=COR_TEXTO_TITULO)
    label_titulo.pack(pady=(24, 16), padx=20, anchor="center")

    linha = tk.Frame(pai, bg=COR_BORDA, height=1)
    linha.pack(fill="x")

    return header


def configurar_estilo_treeview():
    estilo = ttk.Style()
    estilo.theme_use("clam")

    estilo.configure(
        "Treeview",
        background=COR_TABELA_LINHA_PAR,
        fieldbackground=COR_TABELA_LINHA_PAR,
        foreground=COR_TEXTO_ESCURO,
        rowheight=30,
        font=FONTE_TABELA,
        borderwidth=0,
    )
    estilo.map(
        "Treeview",
        background=[("selected", COR_TABELA_SELECAO)],
        foreground=[("selected", "#FFFFFF")],
    )
    estilo.configure(
        "Treeview.Heading",
        font=FONTE_TABELA_HEADER,
        background=COR_TABELA_HEADER_BG,
        foreground=COR_TABELA_HEADER_FG,
        relief="flat",
        borderwidth=0,
        padding=8,
    )
    estilo.map("Treeview.Heading", background=[("active", COR_TABELA_HEADER_BG)])
    estilo.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])


# ==========================================================
#  TELA 1 — FICHA TÉCNICA (formulário completo)
# ==========================================================

def _linha_campo(pai, rotulo, largura_rotulo=12):
    linha = tk.Frame(pai, bg=COR_FUNDO_PRINCIPAL)
    linha.pack(fill="x", pady=4)
    tk.Label(linha, text=rotulo, font=FONTE_ENTRY, bg=COR_FUNDO_PRINCIPAL,
              fg=COR_TEXTO_ESCURO, width=largura_rotulo, anchor="w").pack(side="left")
    entry = tk.Entry(linha, font=FONTE_ENTRY, relief="flat", highlightthickness=1,
                      highlightbackground=COR_BORDA, highlightcolor=COR_TEXTO_ESCURO)
    entry.pack(side="left", fill="x", expand=True, ipady=3)
    return entry


def tela_ficha(ficha_id=None):
    global ficha_atual_id, imagem_atual_path, imagem_tk_ref, label_imagem
    global entry_busca_ficha, entry_preparo, entry_profissional
    global entry_criacao, entry_atualizacao, entry_rendimento
    global text_modo_preparo, tabela_insumos, label_total_valor

    limpar_janela()
    ficha_atual_id = ficha_id
    imagem_atual_path = None
    imagem_tk_ref = None

    frame = tk.Frame(janela, bg=COR_FUNDO_PRINCIPAL)
    frame.pack(fill="both", expand=True)

    criar_header(frame, "Ficha Técnica de Preparo")

    # -------- barra de menu --------
    frame_menu = tk.Frame(frame, bg=COR_FUNDO_MENU)
    frame_menu.pack(fill="x", padx=20, pady=(16, 8))
    interno = tk.Frame(frame_menu, bg=COR_FUNDO_MENU)
    interno.pack(anchor="w", pady=4)

    entry_busca_ficha = tk.Entry(interno, font=FONTE_ENTRY, width=20, relief="flat",
                                  highlightthickness=1, highlightbackground=COR_BORDA,
                                  highlightcolor=COR_TEXTO_ESCURO)
    entry_busca_ficha.pack(side="left", padx=(0, 8), pady=5, ipady=5)

    criar_botao_secundario(interno, "Pesquisar", pesquisar_ficha).pack(side="left", padx=4, pady=5)
    criar_botao(interno, "Cadastrar Novo", lambda: tela_ficha(None)).pack(side="left", padx=4, pady=5)
    criar_botao_secundario(interno, "Ingredientes", tela_ingredientes).pack(side="left", padx=4, pady=5)
    criar_botao_secundario(interno, "Editar", habilitar_edicao_ficha).pack(side="left", padx=4, pady=5)
    criar_botao_secundario(interno, "Excluir", excluir_ficha).pack(side="left", padx=4, pady=5)
    criar_botao_secundario(interno, "Imprimir", imprimir_ficha).pack(side="left", padx=4, pady=5)

    # -------- imagem + campos principais --------
    frame_topo = tk.Frame(frame, bg=COR_FUNDO_PRINCIPAL)
    frame_topo.pack(fill="x", padx=20, pady=8)

    frame_imagem = tk.Frame(frame_topo, bg=COR_IMAGEM_PLACEHOLDER, width=180, height=180,
                             highlightthickness=1, highlightbackground=COR_BORDA)
    frame_imagem.pack(side="left")
    frame_imagem.pack_propagate(False)
    label_imagem = tk.Label(frame_imagem, text="Inserir Imagem", bg=COR_IMAGEM_PLACEHOLDER,
                             fg=COR_TEXTO_ESCURO, cursor="hand2")
    label_imagem.pack(expand=True)
    label_imagem.bind("<Button-1>", lambda e: selecionar_imagem())

    frame_campos = tk.Frame(frame_topo, bg=COR_FUNDO_PRINCIPAL)
    frame_campos.pack(side="left", fill="x", expand=True, padx=20)

    entry_preparo = _linha_campo(frame_campos, "Preparo")
    entry_profissional = _linha_campo(frame_campos, "Profissional")

    frame_datas = tk.Frame(frame_campos, bg=COR_FUNDO_PRINCIPAL)
    frame_datas.pack(fill="x", pady=4)
    tk.Label(frame_datas, text="Criação", font=FONTE_ENTRY, bg=COR_FUNDO_PRINCIPAL,
              fg=COR_TEXTO_ESCURO, width=12, anchor="w").pack(side="left")
    entry_criacao = tk.Entry(frame_datas, font=FONTE_ENTRY, width=12, relief="flat",
                              highlightthickness=1, highlightbackground=COR_BORDA, state="readonly")
    entry_criacao.pack(side="left", padx=(0, 20), ipady=3)
    tk.Label(frame_datas, text="Atualização", font=FONTE_ENTRY, bg=COR_FUNDO_PRINCIPAL,
              fg=COR_TEXTO_ESCURO, anchor="w").pack(side="left")
    entry_atualizacao = tk.Entry(frame_datas, font=FONTE_ENTRY, width=12, relief="flat",
                                  highlightthickness=1, highlightbackground=COR_BORDA, state="readonly")
    entry_atualizacao.pack(side="left", padx=8, ipady=3)

    # -------- insumos --------
    tk.Label(frame, text="Insumos", font=FONTE_TITULO, bg=COR_FUNDO_PRINCIPAL,
              fg=COR_TEXTO_TITULO).pack(pady=(16, 4))

    frame_botoes_insumo = tk.Frame(frame, bg=COR_FUNDO_PRINCIPAL)
    frame_botoes_insumo.pack()
    criar_botao_secundario(frame_botoes_insumo, "+ Adicionar Insumo", abrir_popup_adicionar_insumo).pack(side="left", padx=4)
    criar_botao_secundario(frame_botoes_insumo, "Editar Insumo", abrir_popup_editar_insumo).pack(side="left", padx=4)
    criar_botao_secundario(frame_botoes_insumo, "Remover Insumo", remover_insumo).pack(side="left", padx=4)

    configurar_estilo_treeview()
    frame_tabela_insumos = tk.Frame(frame, bg=COR_BORDA, padx=1, pady=1)
    frame_tabela_insumos.pack(fill="x", padx=20, pady=8)

    colunas = ("ingrediente", "qtd_comprada", "valor_comprado", "qtd_usada", "unidade", "valor_usado")
    titulos = {"ingrediente": "Ingrediente", "qtd_comprada": "Quant\nComprada",
               "valor_comprado": "Valor\nComprado", "qtd_usada": "Quant\nUsada",
               "unidade": "Unidade", "valor_usado": "Valor\nUsado"}
    larguras = {"ingrediente": 220, "qtd_comprada": 90, "valor_comprado": 90,
                "qtd_usada": 90, "unidade": 80, "valor_usado": 90}

    tabela_insumos = ttk.Treeview(frame_tabela_insumos, columns=colunas, show="headings", height=4)
    for c in colunas:
        tabela_insumos.heading(c, text=titulos[c])
        tabela_insumos.column(c, width=larguras[c], anchor="w" if c == "ingrediente" else "center")
    tabela_insumos.tag_configure("par", background=COR_TABELA_LINHA_PAR)
    tabela_insumos.tag_configure("impar", background=COR_TABELA_LINHA_IMPAR)
    tabela_insumos.pack(fill="x", padx=8, pady=8)

    frame_total = tk.Frame(frame, bg=COR_FUNDO_MENU, highlightthickness=1, highlightbackground=COR_BORDA)
    frame_total.pack(fill="x", padx=20)
    tk.Label(frame_total, text="Total do Valor Usado", font=FONTE_TABELA_HEADER,
              bg=COR_FUNDO_MENU, fg=COR_TEXTO_TITULO).pack(side="left", padx=12, pady=8)
    label_total_valor = tk.Label(frame_total, text="0,00", font=FONTE_TABELA_HEADER,
                                  bg=COR_FUNDO_MENU, fg=COR_TEXTO_TITULO)
    label_total_valor.pack(side="right", padx=12, pady=8)

    # -------- modo de preparo --------
    tk.Label(frame, text="Modo de Preparo", font=FONTE_TITULO, bg=COR_FUNDO_PRINCIPAL,
              fg=COR_TEXTO_TITULO).pack(pady=(16, 4))
    frame_modo = tk.Frame(frame, bg=COR_BORDA, padx=1, pady=1)
    frame_modo.pack(fill="x", padx=20)
    text_modo_preparo = tk.Text(frame_modo, height=5, font=FONTE_ENTRY, relief="flat", wrap="word")
    text_modo_preparo.pack(fill="x")

    frame_rendimento = tk.Frame(frame, bg=COR_FUNDO_PRINCIPAL)
    frame_rendimento.pack(fill="x", padx=20, pady=8)
    tk.Label(frame_rendimento, text="Rendimento", font=FONTE_ENTRY, bg=COR_FUNDO_PRINCIPAL,
              fg=COR_TEXTO_ESCURO).pack(side="left")
    entry_rendimento = tk.Entry(frame_rendimento, font=FONTE_ENTRY, relief="flat",
                                 highlightthickness=1, highlightbackground=COR_BORDA)
    entry_rendimento.pack(side="left", padx=8, ipady=3, fill="x", expand=True)

    criar_botao(frame, "Salvar Alteração", salvar_ficha).pack(pady=16)

    if ficha_id:
        carregar_ficha(ficha_id)
    else:
        entry_criacao.config(state="normal")
        entry_criacao.delete(0, tk.END)
        entry_criacao.insert(0, date.today().strftime("%d/%m/%Y"))
        entry_criacao.config(state="readonly")


def habilitar_edicao_ficha():
    entry_preparo.focus_set()


def imprimir_ficha():
    messagebox.showinfo("Imprimir", "Função de impressão em desenvolvimento.")


# -------- imagem --------
def selecionar_imagem():
    global imagem_atual_path
    caminho = filedialog.askopenfilename(
        title="Selecionar imagem",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif")]
    )
    if not caminho:
        return
    imagem_atual_path = caminho
    exibir_imagem(caminho)


def exibir_imagem(caminho):
    global imagem_tk_ref
    try:
        if PIL_OK:
            img = Image.open(caminho)
            img.thumbnail((176, 176))
            imagem_tk_ref = ImageTk.PhotoImage(img)
        else:
            imagem_tk_ref = tk.PhotoImage(file=caminho)
        label_imagem.config(image=imagem_tk_ref, text="")
    except Exception:
        label_imagem.config(text="Imagem inválida", image="")


# -------- carregar / salvar ficha --------
def carregar_ficha(ficha_id):
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("""SELECT preparo, profissional, criacao, atualizacao,
                              imagem_path, modo_preparo, rendimento
                       FROM fichas WHERE id = ?""", (ficha_id,))
    dados = cursor.fetchone()
    conexao.close()

    if not dados:
        messagebox.showerror("Erro", "Ficha não encontrada.")
        return

    preparo, profissional, criacao, atualizacao, imagem_path, modo_preparo, rendimento = dados

    entry_preparo.insert(0, preparo or "")
    entry_profissional.insert(0, profissional or "")

    entry_criacao.config(state="normal")
    entry_criacao.delete(0, tk.END)
    entry_criacao.insert(0, criacao or "")
    entry_criacao.config(state="readonly")

    entry_atualizacao.config(state="normal")
    entry_atualizacao.delete(0, tk.END)
    entry_atualizacao.insert(0, atualizacao or "")
    entry_atualizacao.config(state="readonly")

    text_modo_preparo.insert("1.0", modo_preparo or "")
    entry_rendimento.insert(0, rendimento or "")

    global imagem_atual_path
    imagem_atual_path = imagem_path
    if imagem_path:
        exibir_imagem(imagem_path)

    atualizar_tabela_insumos(ficha_id)


def salvar_ficha():
    global ficha_atual_id

    preparo = entry_preparo.get().strip()
    if not preparo:
        messagebox.showwarning("Aviso", "O campo 'Preparo' não pode ficar vazio!")
        return

    profissional = entry_profissional.get().strip()
    modo_preparo = text_modo_preparo.get("1.0", tk.END).strip()
    rendimento = entry_rendimento.get().strip()
    hoje = date.today().strftime("%d/%m/%Y")

    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()

    if ficha_atual_id is None:
        cursor.execute("""INSERT INTO fichas
            (preparo, profissional, criacao, atualizacao, imagem_path, modo_preparo, rendimento)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (preparo, profissional, hoje, hoje, imagem_atual_path, modo_preparo, rendimento))
        ficha_atual_id = cursor.lastrowid
    else:
        cursor.execute("""UPDATE fichas SET preparo=?, profissional=?, atualizacao=?,
                           imagem_path=?, modo_preparo=?, rendimento=? WHERE id=?""",
            (preparo, profissional, hoje, imagem_atual_path, modo_preparo, rendimento, ficha_atual_id))

    conexao.commit()
    conexao.close()

    entry_atualizacao.config(state="normal")
    entry_atualizacao.delete(0, tk.END)
    entry_atualizacao.insert(0, hoje)
    entry_atualizacao.config(state="readonly")

    messagebox.showinfo("Sucesso", "Ficha salva com sucesso!")


def excluir_ficha():
    if ficha_atual_id is None:
        messagebox.showwarning("Aviso", "Nenhuma ficha carregada para excluir.")
        return

    if not messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir esta ficha?"):
        return

    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM insumos WHERE ficha_id = ?", (ficha_atual_id,))
    cursor.execute("DELETE FROM fichas WHERE id = ?", (ficha_atual_id,))
    conexao.commit()
    conexao.close()

    messagebox.showinfo("Sucesso", "Ficha excluída com sucesso!")
    tela_ficha(None)


# -------- busca de fichas --------
def pesquisar_ficha():
    termo = entry_busca_ficha.get().strip()

    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    if termo:
        cursor.execute("SELECT id, preparo FROM fichas WHERE preparo LIKE ?", ("%" + termo + "%",))
    else:
        cursor.execute("SELECT id, preparo FROM fichas")
    resultados = cursor.fetchall()
    conexao.close()

    tela_resultado_busca(resultados)


def tela_resultado_busca(resultados):
    limpar_janela()

    frame = tk.Frame(janela, bg=COR_FUNDO_PRINCIPAL)
    frame.pack(fill="both", expand=True)

    criar_header(frame, "Ficha Técnica de Preparo")

    frame_menu = tk.Frame(frame, bg=COR_FUNDO_MENU)
    frame_menu.pack(fill="x", padx=20, pady=(16, 8))
    interno = tk.Frame(frame_menu, bg=COR_FUNDO_MENU)
    interno.pack(anchor="center", pady=4)

    entrada = tk.Entry(interno, font=FONTE_ENTRY, width=18, relief="flat",
                        highlightthickness=1, highlightbackground=COR_BORDA)
    entrada.pack(side="left", padx=(0, 8), pady=5, ipady=5)

    def pesquisar_novamente():
        global entry_busca_ficha
        entry_busca_ficha = entrada
        pesquisar_ficha()

    criar_botao_secundario(interno, "Pesquisar", pesquisar_novamente).pack(side="left", padx=4)
    criar_botao(interno, "Cadastrar Novo", lambda: tela_ficha(None)).pack(side="left", padx=4)

    tk.Label(frame, text="Resultado", font=FONTE_TITULO, bg=COR_FUNDO_PRINCIPAL,
              fg=COR_TEXTO_TITULO).pack(pady=(20, 2))
    tk.Label(frame, text=f"{len(resultados)} preparos encontrados", font=FONTE_SUBTITULO,
              bg=COR_FUNDO_PRINCIPAL, fg=COR_TEXTO_SUBTITULO).pack(pady=(0, 16))

    frame_lista = tk.Frame(frame, bg=COR_FUNDO_PRINCIPAL)
    frame_lista.pack(fill="both", expand=True, padx=40)

    if not resultados:
        tk.Label(frame_lista, text="Nenhum preparo encontrado.", font=FONTE_ENTRY,
                  bg=COR_FUNDO_PRINCIPAL, fg=COR_TEXTO_SUBTITULO).pack(anchor="w", pady=4)

    for id_ficha, nome in resultados:
        item = tk.Label(frame_lista, text=nome, font=FONTE_ENTRY, bg=COR_FUNDO_PRINCIPAL,
                         fg=COR_TEXTO_ESCURO, cursor="hand2", anchor="w")
        item.pack(fill="x", pady=6)
        item.bind("<Button-1>", lambda e, fid=id_ficha: tela_ficha(fid))
        item.bind("<Enter>", lambda e, w=item: w.config(fg=COR_ACCENT))
        item.bind("<Leave>", lambda e, w=item: w.config(fg=COR_TEXTO_ESCURO))

    criar_botao(frame, "Voltar", lambda: tela_ficha(None)).pack(pady=16, anchor="e", padx=20)


# ==========================================================
#  INSUMOS (linhas de ingrediente dentro de uma ficha)
# ==========================================================

def _formatar_moeda(valor):
    try:
        return f"{float(valor):.2f}".replace(".", ",")
    except (TypeError, ValueError):
        return "0,00"


def atualizar_tabela_insumos(ficha_id):
    for item in tabela_insumos.get_children():
        tabela_insumos.delete(item)

    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("""SELECT id, ingrediente, quantidade_comprada, valor_comprado,
                              quantidade_usada, unidade_medida, valor_gasto
                       FROM insumos WHERE ficha_id = ?""", (ficha_id,))
    linhas = cursor.fetchall()
    conexao.close()

    for i, (id_insumo, ingrediente, qc, vc, qu, un, vg) in enumerate(linhas):
        tag = "par" if i % 2 == 0 else "impar"
        tabela_insumos.insert("", tk.END, iid=str(id_insumo), tags=(tag,),
                               values=(ingrediente, qc, _formatar_moeda(vc), qu, un or "", _formatar_moeda(vg)))

    recalcular_total_insumos()


def recalcular_total_insumos():
    total = 0.0
    for item in tabela_insumos.get_children():
        valores = tabela_insumos.item(item, "values")
        try:
            total += float(str(valores[5]).replace(",", "."))
        except (ValueError, IndexError):
            pass
    label_total_valor.config(text=_formatar_moeda(total))


def _popup_insumo(titulo, dados_iniciais, ao_salvar):
    """Popup compartilhado por adicionar/editar insumo."""
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT ingrediente, unidade_medida FROM ingredientes ORDER BY ingrediente")
    ingredientes_cadastrados = cursor.fetchall()
    conexao.close()

    mapa_unidades = {nome: unidade for nome, unidade in ingredientes_cadastrados}
    nomes = list(mapa_unidades.keys())

    popup = tk.Toplevel()
    popup.title(titulo)
    popup.geometry("340x380")
    popup.configure(bg=COR_FUNDO_PRINCIPAL)
    popup.grab_set()

    def _campo(rotulo):
        tk.Label(popup, text=rotulo, font=("Segoe UI", 10), bg=COR_FUNDO_PRINCIPAL,
                  fg=COR_TEXTO_ESCURO).pack(anchor="w", padx=20, pady=(10, 2))
        entrada = tk.Entry(popup, font=FONTE_ENTRY, relief="flat", highlightthickness=1,
                            highlightbackground=COR_BORDA)
        entrada.pack(fill="x", padx=20, ipady=4)
        return entrada

    tk.Label(popup, text="Ingrediente", font=("Segoe UI", 10), bg=COR_FUNDO_PRINCIPAL,
              fg=COR_TEXTO_ESCURO).pack(anchor="w", padx=20, pady=(10, 2))
    combo_ingrediente = ttk.Combobox(popup, values=nomes, state="readonly", font=FONTE_ENTRY)
    combo_ingrediente.pack(fill="x", padx=20, ipady=2)

    entry_unidade = _campo("Unidade de Medida")
    entry_unidade.config(state="readonly")

    entry_qtd_comprada = _campo("Quantidade Comprada")
    entry_valor_comprado = _campo("Valor Comprado (R$)")
    entry_qtd_usada = _campo("Quantidade Usada")

    def ao_escolher_ingrediente(event=None):
        unidade = mapa_unidades.get(combo_ingrediente.get(), "") or ""
        entry_unidade.config(state="normal")
        entry_unidade.delete(0, tk.END)
        entry_unidade.insert(0, unidade)
        entry_unidade.config(state="readonly")

    combo_ingrediente.bind("<<ComboboxSelected>>", ao_escolher_ingrediente)

    if dados_iniciais:
        combo_ingrediente.set(dados_iniciais.get("ingrediente", ""))
        ao_escolher_ingrediente()
        entry_qtd_comprada.insert(0, dados_iniciais.get("qtd_comprada", ""))
        entry_valor_comprado.insert(0, dados_iniciais.get("valor_comprado", ""))
        entry_qtd_usada.insert(0, dados_iniciais.get("qtd_usada", ""))

    def salvar():
        ingrediente = combo_ingrediente.get().strip()
        if not ingrediente:
            messagebox.showwarning("Aviso", "Selecione um ingrediente cadastrado.")
            return
        try:
            qtd_comprada = float(entry_qtd_comprada.get().replace(",", ".") or 0)
            valor_comprado = float(entry_valor_comprado.get().replace(",", ".") or 0)
            qtd_usada = float(entry_qtd_usada.get().replace(",", ".") or 0)
        except ValueError:
            messagebox.showwarning("Aviso", "Quantidade e valor devem ser números.")
            return

        valor_gasto = (valor_comprado / qtd_comprada) * qtd_usada if qtd_comprada else 0
        unidade = mapa_unidades.get(ingrediente, "")

        ao_salvar(ingrediente, qtd_comprada, valor_comprado, qtd_usada, unidade, valor_gasto)
        popup.destroy()

    criar_botao(popup, "Salvar", salvar).pack(pady=18)


def abrir_popup_adicionar_insumo():
    if ficha_atual_id is None:
        messagebox.showwarning("Aviso", "Salve a ficha antes de adicionar insumos.")
        return

    def salvar(ingrediente, qc, vc, qu, unidade, vg):
        conexao = sqlite3.connect("ficha_tecnica.db")
        cursor = conexao.cursor()
        cursor.execute("""INSERT INTO insumos
            (ficha_id, ingrediente, quantidade_comprada, valor_comprado,
             quantidade_usada, unidade_medida, valor_gasto)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (ficha_atual_id, ingrediente, qc, vc, qu, unidade, vg))
        conexao.commit()
        conexao.close()
        atualizar_tabela_insumos(ficha_atual_id)
        messagebox.showinfo("Sucesso", "Insumo adicionado com sucesso!")

    _popup_insumo("Adicionar Insumo", None, salvar)


def abrir_popup_editar_insumo():
    selecao = tabela_insumos.selection()
    if not selecao:
        messagebox.showwarning("Aviso", "Selecione um insumo para editar.")
        return

    id_insumo = selecao[0]
    valores = tabela_insumos.item(id_insumo, "values")
    dados_iniciais = {
        "ingrediente": valores[0],
        "qtd_comprada": valores[1],
        "valor_comprado": str(valores[2]).replace(",", "."),
        "qtd_usada": valores[3],
    }

    def salvar(ingrediente, qc, vc, qu, unidade, vg):
        conexao = sqlite3.connect("ficha_tecnica.db")
        cursor = conexao.cursor()
        cursor.execute("""UPDATE insumos SET ingrediente=?, quantidade_comprada=?, valor_comprado=?,
                           quantidade_usada=?, unidade_medida=?, valor_gasto=? WHERE id=?""",
            (ingrediente, qc, vc, qu, unidade, vg, id_insumo))
        conexao.commit()
        conexao.close()
        atualizar_tabela_insumos(ficha_atual_id)
        messagebox.showinfo("Sucesso", "Insumo atualizado com sucesso!")

    _popup_insumo("Editar Insumo", dados_iniciais, salvar)


def remover_insumo():
    selecao = tabela_insumos.selection()
    if not selecao:
        messagebox.showwarning("Aviso", "Selecione um insumo para remover.")
        return

    if not messagebox.askyesno("Confirmar", "Deseja remover o(s) insumo(s) selecionado(s)?"):
        return

    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    for id_insumo in selecao:
        cursor.execute("DELETE FROM insumos WHERE id = ?", (id_insumo,))
    conexao.commit()
    conexao.close()

    atualizar_tabela_insumos(ficha_atual_id)


# ==========================================================
#  TELA 3 — INGREDIENTES (cadastro mestre, com ícones de ação)
# ==========================================================

def pesquisar_ingrediente():
    termo = entry_busca_ingrediente.get().strip()

    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    if termo:
        cursor.execute("SELECT id, ingrediente, unidade_medida FROM ingredientes WHERE ingrediente LIKE ?",
                        ("%" + termo + "%",))
    else:
        cursor.execute("SELECT id, ingrediente, unidade_medida FROM ingredientes")
    resultado = cursor.fetchall()
    conexao.close()

    if not resultado:
        messagebox.showinfo("Informação", "Nenhum ingrediente encontrado com esse termo.")

    montar_lista_ingredientes(resultado)


def limpar_lista_ingredientes():
    for widget in frame_linhas_ingredientes.winfo_children():
        widget.destroy()


def montar_lista_ingredientes(linhas):
    limpar_lista_ingredientes()
    for i, (id_ing, nome, unidade) in enumerate(linhas):
        bg = COR_TABELA_LINHA_PAR if i % 2 == 0 else COR_TABELA_LINHA_IMPAR
        linha = tk.Frame(frame_linhas_ingredientes, bg=bg)
        linha.pack(fill="x")

        tk.Label(linha, text=nome, font=FONTE_TABELA, bg=bg, fg=COR_TEXTO_ESCURO,
                  width=32, anchor="w", padx=8, pady=8).pack(side="left")
        tk.Label(linha, text=unidade or "", font=FONTE_TABELA, bg=bg, fg=COR_TEXTO_ESCURO,
                  width=14, anchor="center").pack(side="left")

        frame_acoes = tk.Frame(linha, bg=bg)
        frame_acoes.pack(side="left", padx=12, pady=40)
        criar_botao_icone(frame_acoes, "Editar", lambda i=id_ing: abrir_popup_editar_ingrediente(i),
                           COR_BOTAO).pack(side="left", padx=3)
        
        # Botão de Excluir
        criar_botao_icone(frame_acoes, "Excluir", lambda i=id_ing: deletar_ingrediente(i),
                           COR_BOTAO_PERIGO).pack(side="left", padx=3)

def atualizar_lista_ingredientes():
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT id, ingrediente, unidade_medida FROM ingredientes")
    linhas = cursor.fetchall()
    conexao.close()
    montar_lista_ingredientes(linhas)


def deletar_ingrediente(id_ingrediente):
    if not messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja deletar este ingrediente?"):
        return

    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM ingredientes WHERE id = ?", (id_ingrediente,))
    conexao.commit()
    conexao.close()

    atualizar_lista_ingredientes()
    messagebox.showinfo("Sucesso", "Ingrediente deletado com sucesso!")


def _popup_ingrediente(titulo, nome_inicial, unidade_inicial, ao_salvar):
    popup = tk.Toplevel()
    popup.title(titulo)
    popup.geometry("320x240")
    popup.configure(bg=COR_FUNDO_PRINCIPAL)
    popup.grab_set()

    tk.Label(popup, text="Nome do Ingrediente:", font=("Segoe UI", 11), bg=COR_FUNDO_PRINCIPAL,
              fg=COR_TEXTO_ESCURO).pack(pady=(18, 8))
    entry_nome = tk.Entry(popup, width=30, font=FONTE_ENTRY, relief="flat", highlightthickness=1,
                           highlightbackground=COR_BORDA, highlightcolor=COR_TEXTO_ESCURO)
    entry_nome.pack(pady=5, ipady=4)
    entry_nome.insert(0, nome_inicial or "")

    tk.Label(popup, text="Unidade de Medida:", font=("Segoe UI", 11), bg=COR_FUNDO_PRINCIPAL,
              fg=COR_TEXTO_ESCURO).pack(pady=(10, 8))
    entry_unidade = tk.Entry(popup, width=30, font=FONTE_ENTRY, relief="flat", highlightthickness=1,
                              highlightbackground=COR_BORDA, highlightcolor=COR_TEXTO_ESCURO)
    entry_unidade.pack(pady=5, ipady=4)
    entry_unidade.insert(0, unidade_inicial or "")

    def salvar():
        nome = entry_nome.get().strip()
        unidade = entry_unidade.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "O campo não pode ficar vazio!")
            return
        ao_salvar(nome, unidade)
        popup.destroy()

    criar_botao(popup, "Salvar", salvar).pack(pady=18)


def abrir_popup_adicionar_ingrediente():
    def salvar(nome, unidade):
        conexao = sqlite3.connect("ficha_tecnica.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO ingredientes (ingrediente, unidade_medida) VALUES (?, ?)", (nome, unidade))
        conexao.commit()
        conexao.close()
        atualizar_lista_ingredientes()
        messagebox.showinfo("Sucesso", "Ingrediente adicionado com sucesso.")

    _popup_ingrediente("Adicionar Ingrediente", "", "", salvar)


def abrir_popup_editar_ingrediente(id_ingrediente):
    conexao = sqlite3.connect("ficha_tecnica.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT ingrediente, unidade_medida FROM ingredientes WHERE id = ?", (id_ingrediente,))
    dados = cursor.fetchone()
    conexao.close()

    if not dados:
        messagebox.showerror("Erro", "Ingrediente não encontrado.")
        return

    nome_atual, unidade_atual = dados

    def salvar(nome, unidade):
        conexao = sqlite3.connect("ficha_tecnica.db")
        cursor = conexao.cursor()
        cursor.execute("UPDATE ingredientes SET ingrediente = ?, unidade_medida = ? WHERE id = ?",
                        (nome, unidade, id_ingrediente))
        conexao.commit()
        conexao.close()
        atualizar_lista_ingredientes()
        messagebox.showinfo("Sucesso", "Ingrediente atualizado com sucesso!")

    _popup_ingrediente("Editar Ingrediente", nome_atual, unidade_atual, salvar)


def tela_ingredientes():
    global entry_busca_ingrediente, frame_linhas_ingredientes

    limpar_janela()

    frame = tk.Frame(janela, bg=COR_FUNDO_PRINCIPAL)
    frame.pack(fill="both", expand=True)

    criar_header(frame, "Ficha Técnica de Preparo")

    frame_menu = tk.Frame(frame, bg=COR_FUNDO_MENU)
    frame_menu.pack(fill="x", padx=20, pady=(16, 8))
    interno = tk.Frame(frame_menu, bg=COR_FUNDO_MENU)
    interno.pack(anchor="center", pady=4)

    entry_busca_ingrediente = tk.Entry(interno, font=FONTE_ENTRY, relief="flat",
                                        highlightthickness=1, highlightbackground=COR_BORDA,
                                        highlightcolor=COR_TEXTO_ESCURO, width=22)
    entry_busca_ingrediente.pack(side="left", padx=(0, 8), pady=5, ipady=5)

    criar_botao_secundario(interno, "Pesquisar", pesquisar_ingrediente).pack(side="left", padx=4, pady=5)
    criar_botao(interno, "+ Adicionar", abrir_popup_adicionar_ingrediente).pack(side="left", padx=4, pady=5)

    # cabeçalho da "tabela"
    frame_tabela = tk.Frame(frame, bg=COR_BORDA, padx=1, pady=1)
    frame_tabela.pack(fill="x", padx=40, pady=(8, 0))
    frame_cabecalho = tk.Frame(frame_tabela, bg=COR_TABELA_HEADER_BG)
    frame_cabecalho.pack(fill="x")
    tk.Label(frame_cabecalho, text="Ingrediente", font=FONTE_TABELA_HEADER, bg=COR_TABELA_HEADER_BG,
              fg=COR_TABELA_HEADER_FG, width=32, anchor="w", padx=8, pady=8).pack(side="left")
    tk.Label(frame_cabecalho, text="Unidade\nde Medida", font=FONTE_TABELA_HEADER, bg=COR_TABELA_HEADER_BG,
              fg=COR_TABELA_HEADER_FG, width=14, anchor="center").pack(side="left")
    tk.Label(frame_cabecalho, text="Ação", font=FONTE_TABELA_HEADER, bg=COR_TABELA_HEADER_BG,
              fg=COR_TABELA_HEADER_FG, width=10, anchor="center").pack(side="left")

    frame_linhas_ingredientes = tk.Frame(frame_tabela, bg=COR_FUNDO_PRINCIPAL)
    frame_linhas_ingredientes.pack(fill="x")

    criar_botao(frame, "Voltar", lambda: tela_ficha(ficha_atual_id)).pack(pady=20, anchor="e", padx=40)

    atualizar_lista_ingredientes()


##########################   INÍCIO   ##########################

conectar_banco_dados()

# cria a janela principal
janela = tk.Tk()
janela.title("Maedu")
janela.geometry("1920x1080")
janela.resizable(False, False)
janela.configure(bg=COR_FUNDO_PRINCIPAL)

tela_ficha()

janela.mainloop()