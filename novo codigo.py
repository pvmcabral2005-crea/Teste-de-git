import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# CONFIGURAÇÕES
# ============================================================

DB_NAME = "ficha_tecnica.db"

CORES = {
    "fundo": "#F4F7FB",
    "branco": "#FFFFFF",
    "sidebar": "#172B4D",
    "sidebar_hover": "#24466F",
    "primaria": "#0F766E",
    "primaria_hover": "#0B5F59",
    "secundaria": "#F59E0B",
    "perigo": "#DC2626",
    "perigo_hover": "#B91C1C",
    "texto": "#172033",
    "texto_secundario": "#64748B",
    "borda": "#DCE3EC",
    "suave": "#EAF3F2",
}


# ============================================================
# BANCO DE DADOS
# ============================================================

def conectar():
    return sqlite3.connect(DB_NAME)


def conectar_banco_dados():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fichas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingrediente TEXT NOT NULL,
            quantidade_comprada REAL,
            valor_comprado REAL,
            quantidade_usada REAL,
            unidade_medida TEXT,
            valor_gasto REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingrediente TEXT NOT NULL UNIQUE
        )
    """)

    conexao.commit()
    conexao.close()


# ============================================================
# APLICAÇÃO
# ============================================================

class FichaTecnicaApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Ficha Técnica de Alimentos")
        self.geometry("1180x720")
        self.minsize(980, 620)
        self.configure(bg=CORES["fundo"])

        self.tabela_ingredientes = None
        self.tabela_fichas = None
        self.entry_busca = None

        self.status_var = tk.StringVar(value="Sistema pronto")

        self._configurar_estilos()
        self._criar_layout()

        self.tela_dashboard()

    # ========================================================
    # ESTILOS
    # ========================================================

    def _configurar_estilos(self):
        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background=CORES["branco"],
            foreground=CORES["texto"],
            fieldbackground=CORES["branco"],
            rowheight=38,
            font=("Segoe UI", 10),
            borderwidth=0,
        )

        estilo.configure(
            "Treeview.Heading",
            background="#E9EEF5",
            foreground=CORES["texto"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            padding=10,
        )

        estilo.map(
            "Treeview",
            background=[("selected", "#D7EFEC")],
            foreground=[("selected", CORES["texto"])],
        )

        estilo.configure(
            "TCombobox",
            padding=8,
            font=("Segoe UI", 10),
        )

    # ========================================================
    # LAYOUT PRINCIPAL
    # ========================================================

    def _criar_layout(self):
        self.sidebar = tk.Frame(
            self,
            bg=CORES["sidebar"],
            width=235
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.conteudo = tk.Frame(
            self,
            bg=CORES["fundo"]
        )
        self.conteudo.pack(side="right", fill="both", expand=True)

        # Logo / título
        logo = tk.Frame(self.sidebar, bg=CORES["sidebar"])
        logo.pack(fill="x", padx=20, pady=(25, 30))

        tk.Label(
            logo,
            text="FICHA+",
            font=("Segoe UI", 22, "bold"),
            fg="#FFFFFF",
            bg=CORES["sidebar"]
        ).pack(anchor="w")

        tk.Label(
            logo,
            text="Gestão de alimentos",
            font=("Segoe UI", 9),
            fg="#AFC2D9",
            bg=CORES["sidebar"]
        ).pack(anchor="w", pady=(2, 0))

        self._botao_menu("Dashboard", self.tela_dashboard)
        self._botao_menu("Ingredientes", self.tela_ingredientes)
        self._botao_menu("Ficha Técnica", self.tela_ficha)

        tk.Frame(
            self.sidebar,
            bg="#315072",
            height=1
        ).pack(fill="x", padx=20, pady=25)

        tk.Label(
            self.sidebar,
            text="RECURSOS",
            font=("Segoe UI", 8, "bold"),
            fg="#7890AB",
            bg=CORES["sidebar"]
        ).pack(anchor="w", padx=22, pady=(0, 10))

        self._botao_menu("Atualizar dados", self.atualizar_dashboard)

        # Rodapé da sidebar
        rodape = tk.Frame(self.sidebar, bg=CORES["sidebar"])
        rodape.pack(side="bottom", fill="x", padx=20, pady=20)

        tk.Label(
            rodape,
            text="SQLite + Tkinter",
            font=("Segoe UI", 9),
            fg="#8FA6BF",
            bg=CORES["sidebar"]
        ).pack(anchor="w")

        tk.Label(
            rodape,
            text="Projeto Integrador Python",
            font=("Segoe UI", 8),
            fg="#647E9B",
            bg=CORES["sidebar"]
        ).pack(anchor="w", pady=(3, 0))

        # Barra superior
        self.topbar = tk.Frame(
            self.conteudo,
            bg=CORES["branco"],
            height=70,
            highlightbackground=CORES["borda"],
            highlightthickness=1
        )
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        self.titulo_pagina = tk.Label(
            self.topbar,
            text="Dashboard",
            font=("Segoe UI", 18, "bold"),
            fg=CORES["texto"],
            bg=CORES["branco"]
        )
        self.titulo_pagina.pack(side="left", padx=30)

        self.status_label = tk.Label(
            self.topbar,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            fg=CORES["texto_secundario"],
            bg=CORES["branco"]
        )
        self.status_label.pack(side="right", padx=30)

        self.area_tela = tk.Frame(
            self.conteudo,
            bg=CORES["fundo"]
        )
        self.area_tela.pack(fill="both", expand=True, padx=28, pady=25)

    def _botao_menu(self, texto, comando):
        botao = tk.Button(
            self.sidebar,
            text=texto,
            command=comando,
            anchor="w",
            padx=22,
            pady=13,
            bd=0,
            relief="flat",
            bg=CORES["sidebar"],
            fg="#DCE7F3",
            activebackground=CORES["sidebar_hover"],
            activeforeground="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        )
        botao.pack(fill="x", padx=10, pady=2)

        botao.bind(
            "<Enter>",
            lambda e: botao.configure(bg=CORES["sidebar_hover"])
        )
        botao.bind(
            "<Leave>",
            lambda e: botao.configure(bg=CORES["sidebar"])
        )

    # ========================================================
    # COMPONENTES VISUAIS
    # ========================================================

    def limpar_area(self):
        for widget in self.area_tela.winfo_children():
            widget.destroy()

    def definir_titulo(self, titulo):
        self.titulo_pagina.config(text=titulo)

    def card(self, parent, titulo, valor, detalhe="", destaque=False):
        frame = tk.Frame(
            parent,
            bg=CORES["branco"],
            highlightbackground=CORES["borda"],
            highlightthickness=1
        )

        topo = tk.Frame(frame, bg=CORES["branco"])
        topo.pack(fill="x", padx=20, pady=(18, 5))

        tk.Label(
            topo,
            text=titulo.upper(),
            font=("Segoe UI", 9, "bold"),
            fg=CORES["texto_secundario"],
            bg=CORES["branco"]
        ).pack(anchor="w")

        tk.Label(
            frame,
            text=valor,
            font=("Segoe UI", 25, "bold"),
            fg=CORES["primaria"] if destaque else CORES["texto"],
            bg=CORES["branco"]
        ).pack(anchor="w", padx=20)

        if detalhe:
            tk.Label(
                frame,
                text=detalhe,
                font=("Segoe UI", 9),
                fg=CORES["texto_secundario"],
                bg=CORES["branco"]
            ).pack(anchor="w", padx=20, pady=(2, 18))
        else:
            tk.Frame(frame, bg=CORES["branco"], height=18).pack()

        return frame

    def botao(self, parent, texto, comando, tipo="primario", largura=14):
        if tipo == "primario":
            bg = CORES["primaria"]
            active = CORES["primaria_hover"]
            fg = "#FFFFFF"
        elif tipo == "perigo":
            bg = CORES["perigo"]
            active = CORES["perigo_hover"]
            fg = "#FFFFFF"
        elif tipo == "secundario":
            bg = "#E8EEF5"
            active = "#D9E2EC"
            fg = CORES["texto"]
        else:
            bg = CORES["branco"]
            active = "#F1F5F9"
            fg = CORES["texto"]

        b = tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=bg,
            activebackground=active,
            fg=fg,
            activeforeground=fg,
            bd=0,
            relief="flat",
            padx=15,
            pady=9,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            width=largura
        )

        return b

    def campo(self, parent, label, variavel=None, largura=30):
        container = tk.Frame(parent, bg=CORES["branco"])

        tk.Label(
            container,
            text=label,
            font=("Segoe UI", 9, "bold"),
            fg=CORES["texto"],
            bg=CORES["branco"]
        ).pack(anchor="w", pady=(0, 6))

        entry = tk.Entry(
            container,
            textvariable=variavel,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            fg=CORES["texto"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=CORES["borda"],
            highlightcolor=CORES["primaria"],
            width=largura,
            insertbackground=CORES["texto"]
        )
        entry.pack(fill="x", ipady=8)

        return container, entry

    # ========================================================
    # DASHBOARD
    # ========================================================

    def tela_dashboard(self):
        self.limpar_area()
        self.definir_titulo("Dashboard")
        self.status_var.set("Visão geral do sistema")

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT COUNT(*) FROM ingredientes")
        total_ingredientes = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM fichas")
        total_fichas = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(valor_gasto), 0) FROM fichas")
        custo_total = cursor.fetchone()[0]

        conexao.close()

        cabecalho = tk.Frame(self.area_tela, bg=CORES["fundo"])
        cabecalho.pack(fill="x")

        tk.Label(
            cabecalho,
            text="Visão geral",
            font=("Segoe UI", 22, "bold"),
            fg=CORES["texto"],
            bg=CORES["fundo"]
        ).pack(anchor="w")

        tk.Label(
            cabecalho,
            text="Acompanhe os principais dados da sua ficha técnica.",
            font=("Segoe UI", 10),
            fg=CORES["texto_secundario"],
            bg=CORES["fundo"]
        ).pack(anchor="w", pady=(3, 20))

        cards = tk.Frame(self.area_tela, bg=CORES["fundo"])
        cards.pack(fill="x")

        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)
        cards.columnconfigure(2, weight=1)

        self.card(
            cards,
            "Ingredientes",
            str(total_ingredientes),
            "cadastrados no sistema",
            True
        ).grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.card(
            cards,
            "Registros da ficha",
            str(total_fichas),
            "lançamentos registrados"
        ).grid(row=0, column=1, sticky="nsew", padx=5)

        self.card(
            cards,
            "Custo registrado",
            f"R$ {custo_total:.2f}",
            "soma dos custos utilizados"
        ).grid(row=0, column=2, sticky="nsew", padx=(10, 0))

        # Área de ações
        acoes = tk.Frame(
            self.area_tela,
            bg=CORES["branco"],
            highlightbackground=CORES["borda"],
            highlightthickness=1
        )
        acoes.pack(fill="x", pady=25)

        tk.Label(
            acoes,
            text="Acesso rápido",
            font=("Segoe UI", 13, "bold"),
            fg=CORES["texto"],
            bg=CORES["branco"]
        ).pack(anchor="w", padx=22, pady=(20, 4))

        tk.Label(
            acoes,
            text="Escolha uma das opções para começar.",
            font=("Segoe UI", 9),
            fg=CORES["texto_secundario"],
            bg=CORES["branco"]
        ).pack(anchor="w", padx=22, pady=(0, 15))

        linha_botoes = tk.Frame(acoes, bg=CORES["branco"])
        linha_botoes.pack(anchor="w", padx=22, pady=(0, 22))

        self.botao(
            linha_botoes,
            "Gerenciar ingredientes",
            self.tela_ingredientes,
            "primario",
            22
        ).pack(side="left", padx=(0, 10))

        self.botao(
            linha_botoes,
            "Abrir ficha técnica",
            self.tela_ficha,
            "secundario",
            22
        ).pack(side="left")

    def atualizar_dashboard(self):
        self.tela_dashboard()

    # ========================================================
    # INGREDIENTES
    # ========================================================

    def tela_ingredientes(self):
        self.limpar_area()
        self.definir_titulo("Ingredientes")
        self.status_var.set("Cadastro e gerenciamento de ingredientes")

        cabecalho = tk.Frame(self.area_tela, bg=CORES["fundo"])
        cabecalho.pack(fill="x")

        tk.Label(
            cabecalho,
            text="Ingredientes",
            font=("Segoe UI", 22, "bold"),
            fg=CORES["texto"],
            bg=CORES["fundo"]
        ).pack(side="left")

        self.botao(
            cabecalho,
            "+ Adicionar ingrediente",
            self.abrir_popup_adicionar,
            "primario",
            20
        ).pack(side="right")

        tk.Label(
            self.area_tela,
            text="Cadastre, pesquise, edite ou remova os ingredientes utilizados nas fichas.",
            font=("Segoe UI", 10),
            fg=CORES["texto_secundario"],
            bg=CORES["fundo"]
        ).pack(anchor="w", pady=(3, 18))

        painel = tk.Frame(
            self.area_tela,
            bg=CORES["branco"],
            highlightbackground=CORES["borda"],
            highlightthickness=1
        )
        painel.pack(fill="both", expand=True)

        barra = tk.Frame(painel, bg=CORES["branco"])
        barra.pack(fill="x", padx=20, pady=18)

        tk.Label(
            barra,
            text="Pesquisar:",
            font=("Segoe UI", 9, "bold"),
            fg=CORES["texto"],
            bg=CORES["branco"]
        ).pack(side="left")

        self.entry_busca = tk.Entry(
            barra,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            relief="flat",
            highlightthickness=1,
            highlightbackground=CORES["borda"],
            width=35
        )
        self.entry_busca.pack(side="left", padx=10, ipady=7)

        self.botao(
            barra,
            "Pesquisar",
            self.pesquisar_ingrediente,
            "secundario",
            12
        ).pack(side="left")

        self.botao(
            barra,
            "Mostrar todos",
            self.atualizar_tabela_ingredientes,
            "secundario",
            13
        ).pack(side="left", padx=8)

        tabela_frame = tk.Frame(painel, bg=CORES["branco"])
        tabela_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tabela_ingredientes = ttk.Treeview(
            tabela_frame,
            columns=("id", "ingrediente"),
            show="headings",
            selectmode="extended"
        )

        self.tabela_ingredientes.heading("id", text="ID")
        self.tabela_ingredientes.heading("ingrediente", text="INGREDIENTE")

        self.tabela_ingredientes.column("id", width=80, anchor="center")
        self.tabela_ingredientes.column("ingrediente", width=500, anchor="w")

        scroll = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tabela_ingredientes.yview
        )
        self.tabela_ingredientes.configure(yscrollcommand=scroll.set)

        self.tabela_ingredientes.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        rodape = tk.Frame(painel, bg=CORES["branco"])
        rodape.pack(fill="x", padx=20, pady=(0, 20))

        self.botao(
            rodape,
            "Editar selecionado",
            self.abrir_popup_editar,
            "secundario",
            18
        ).pack(side="left")

        self.botao(
            rodape,
            "Excluir selecionado",
            self.deletar_ingrediente,
            "perigo",
            18
        ).pack(side="left", padx=8)

        self.atualizar_tabela_ingredientes()

    def atualizar_tabela_ingredientes(self):
        if self.tabela_ingredientes is None:
            return

        for item in self.tabela_ingredientes.get_children():
            self.tabela_ingredientes.delete(item)

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id, ingrediente FROM ingredientes ORDER BY ingrediente"
        )
        dados = cursor.fetchall()
        conexao.close()

        for linha in dados:
            self.tabela_ingredientes.insert("", "end", values=linha)

        self.status_var.set(f"{len(dados)} ingrediente(s) cadastrado(s)")

    def pesquisar_ingrediente(self):
        termo = self.entry_busca.get().strip()

        if not termo:
            self.atualizar_tabela_ingredientes()
            return

        for item in self.tabela_ingredientes.get_children():
            self.tabela_ingredientes.delete(item)

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            SELECT id, ingrediente
            FROM ingredientes
            WHERE ingrediente LIKE ?
            ORDER BY ingrediente
            """,
            (f"%{termo}%",)
        )

        dados = cursor.fetchall()
        conexao.close()

        for linha in dados:
            self.tabela_ingredientes.insert("", "end", values=linha)

        self.status_var.set(f"{len(dados)} resultado(s) encontrado(s)")

        if not dados:
            messagebox.showinfo(
                "Pesquisa",
                "Nenhum ingrediente foi encontrado."
            )

    def abrir_popup_adicionar(self):
        popup = tk.Toplevel(self)
        popup.title("Adicionar ingrediente")
        popup.geometry("430x250")
        popup.resizable(False, False)
        popup.configure(bg=CORES["branco"])
        popup.transient(self)
        popup.grab_set()

        tk.Label(
            popup,
            text="Novo ingrediente",
            font=("Segoe UI", 17, "bold"),
            fg=CORES["texto"],
            bg=CORES["branco"]
        ).pack(anchor="w", padx=30, pady=(25, 4))

        tk.Label(
            popup,
            text="Informe o nome do ingrediente.",
            font=("Segoe UI", 9),
            fg=CORES["texto_secundario"],
            bg=CORES["branco"]
        ).pack(anchor="w", padx=30, pady=(0, 15))

        entry = tk.Entry(
            popup,
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            relief="flat",
            highlightthickness=1,
            highlightbackground=CORES["borda"]
        )
        entry.pack(fill="x", padx=30, ipady=9)
        entry.focus()

        def salvar():
            nome = entry.get().strip()

            if not nome:
                messagebox.showwarning(
                    "Atenção",
                    "Informe o nome do ingrediente.",
                    parent=popup
                )
                return

            try:
                conexao = conectar()
                cursor = conexao.cursor()
                cursor.execute(
                    "INSERT INTO ingredientes (ingrediente) VALUES (?)",
                    (nome,)
                )
                conexao.commit()
                conexao.close()

                popup.destroy()
                self.atualizar_tabela_ingredientes()
                messagebox.showinfo(
                    "Sucesso",
                    "Ingrediente cadastrado com sucesso."
                )
            except sqlite3.IntegrityError:
                messagebox.showwarning(
                    "Atenção",
                    "Esse ingrediente já está cadastrado.",
                    parent=popup
                )

        botoes = tk.Frame(popup, bg=CORES["branco"])
        botoes.pack(fill="x", padx=30, pady=22)

        self.botao(
            botoes,
            "Cancelar",
            popup.destroy,
            "secundario",
            12
        ).pack(side="right")

        self.botao(
            botoes,
            "Salvar",
            salvar,
            "primario",
            12
        ).pack(side="right", padx=8)

    def abrir_popup_editar(self):
        selecao = self.tabela_ingredientes.selection()

        if not selecao:
            messagebox.showwarning(
                "Atenção",
                "Selecione um ingrediente para editar."
            )
            return

        item = selecao[0]
        valores = self.tabela_ingredientes.item(item, "values")
        id_ingrediente = valores[0]
        nome_atual = valores[1]

        popup = tk.Toplevel(self)
        popup.title("Editar ingrediente")
        popup.geometry("430x250")
        popup.resizable(False, False)
        popup.configure(bg=CORES["branco"])
        popup.transient(self)
        popup.grab_set()

        tk.Label(
            popup,
            text="Editar ingrediente",
            font=("Segoe UI", 17, "bold"),
            fg=CORES["texto"],
            bg=CORES["branco"]
        ).pack(anchor="w", padx=30, pady=(25, 4))

        tk.Label(
            popup,
            text="Altere o nome e confirme a operação.",
            font=("Segoe UI", 9),
            fg=CORES["texto_secundario"],
            bg=CORES["branco"]
        ).pack(anchor="w", padx=30, pady=(0, 15))

        entry = tk.Entry(
            popup,
            font=("Segoe UI", 11),
            bg="#F8FAFC",
            relief="flat",
            highlightthickness=1,
            highlightbackground=CORES["borda"]
        )
        entry.pack(fill="x", padx=30, ipady=9)
        entry.insert(0, nome_atual)
        entry.focus()
        entry.select_range(0, tk.END)

        def salvar():
            novo_nome = entry.get().strip()

            if not novo_nome:
                messagebox.showwarning(
                    "Atenção",
                    "O nome não pode ficar vazio.",
                    parent=popup
                )
                return

            try:
                conexao = conectar()
                cursor = conexao.cursor()
                cursor.execute(
                    """
                    UPDATE ingredientes
                    SET ingrediente = ?
                    WHERE id = ?
                    """,
                    (novo_nome, id_ingrediente)
                )
                conexao.commit()
                conexao.close()

                popup.destroy()
                self.atualizar_tabela_ingredientes()
                messagebox.showinfo(
                    "Sucesso",
                    "Ingrediente atualizado com sucesso."
                )
            except sqlite3.IntegrityError:
                messagebox.showwarning(
                    "Atenção",
                    "Já existe outro ingrediente com esse nome.",
                    parent=popup
                )

        botoes = tk.Frame(popup, bg=CORES["branco"])
        botoes.pack(fill="x", padx=30, pady=22)

        self.botao(
            botoes,
            "Cancelar",
            popup.destroy,
            "secundario",
            12
        ).pack(side="right")

        self.botao(
            botoes,
            "Salvar alterações",
            salvar,
            "primario",
            16
        ).pack(side="right", padx=8)

    def deletar_ingrediente(self):
        selecao = self.tabela_ingredientes.selection()

        if not selecao:
            messagebox.showwarning(
                "Atenção",
                "Selecione pelo menos um ingrediente."
            )
            return

        quantidade = len(selecao)

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir {quantidade} ingrediente(s)?"
        )

        if not confirmar:
            return

        conexao = conectar()
        cursor = conexao.cursor()

        for item in selecao:
            valores = self.tabela_ingredientes.item(item, "values")
            id_ingrediente = valores[0]

            cursor.execute(
                "DELETE FROM ingredientes WHERE id = ?",
                (id_ingrediente,)
            )

        conexao.commit()
        conexao.close()

        self.atualizar_tabela_ingredientes()

        messagebox.showinfo(
            "Sucesso",
            "Ingrediente(s) excluído(s) com sucesso."
        )

    # ========================================================
    # FICHA TÉCNICA
    # ========================================================

    def tela_ficha(self):
        self.limpar_area()
        self.definir_titulo("Ficha Técnica")
        self.status_var.set("Controle de custos e quantidades")

        cabecalho = tk.Frame(self.area_tela, bg=CORES["fundo"])
        cabecalho.pack(fill="x")

        tk.Label(
            cabecalho,
            text="Ficha Técnica de Preparo",
            font=("Segoe UI", 22, "bold"),
            fg=CORES["texto"],
            bg=CORES["fundo"]
        ).pack(side="left")

        self.botao(
            cabecalho,
            "+ Novo lançamento",
            self.abrir_popup_ficha,
            "primario",
            18
        ).pack(side="right")

        tk.Label(
            self.area_tela,
            text="Registre ingredientes, quantidades, unidade de medida e custo utilizado.",
            font=("Segoe UI", 10),
            fg=CORES["texto_secundario"],
            bg=CORES["fundo"]
        ).pack(anchor="w", pady=(3, 18))

        painel = tk.Frame(
            self.area_tela,
            bg=CORES["branco"],
            highlightbackground=CORES["borda"],
            highlightthickness=1
        )
        painel.pack(fill="both", expand=True)

        tabela_frame = tk.Frame(painel, bg=CORES["branco"])
        tabela_frame.pack(fill="both", expand=True, padx=20, pady=20)

        colunas = (
            "id",
            "ingrediente",
            "qtd_comprada",
            "valor_comprado",
            "qtd_usada",
            "unidade",
            "valor_gasto"
        )

        self.tabela_fichas = ttk.Treeview(
            tabela_frame,
            columns=colunas,
            show="headings"
        )

        cabecalhos = {
            "id": "ID",
            "ingrediente": "INGREDIENTE",
            "qtd_comprada": "QTD. COMPRADA",
            "valor_comprado": "VALOR COMPRA",
            "qtd_usada": "QTD. USADA",
            "unidade": "UNIDADE",
            "valor_gasto": "CUSTO USADO"
        }

        larguras = {
            "id": 55,
            "ingrediente": 220,
            "qtd_comprada": 120,
            "valor_comprado": 120,
            "qtd_usada": 110,
            "unidade": 90,
            "valor_gasto": 110
        }

        for coluna in colunas:
            self.tabela_fichas.heading(
                coluna,
                text=cabecalhos[coluna]
            )
            self.tabela_fichas.column(
                coluna,
                width=larguras[coluna],
                anchor="center"
            )

        scroll_y = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tabela_fichas.yview
        )

        self.tabela_fichas.configure(
            yscrollcommand=scroll_y.set
        )

        self.tabela_fichas.pack(
            side="left",
            fill="both",
            expand=True
        )
        scroll_y.pack(side="right", fill="y")

        rodape = tk.Frame(painel, bg=CORES["branco"])
        rodape.pack(fill="x", padx=20, pady=(0, 20))

        self.botao(
            rodape,
            "Excluir lançamento",
            self.deletar_ficha,
            "perigo",
            18
        ).pack(side="left")

        self.atualizar_tabela_fichas()

    def atualizar_tabela_fichas(self):
        if self.tabela_fichas is None:
            return

        for item in self.tabela_fichas.get_children():
            self.tabela_fichas.delete(item)

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id,
                ingrediente,
                quantidade_comprada,
                valor_comprado,
                quantidade_usada,
                unidade_medida,
                valor_gasto
            FROM fichas
            ORDER BY id DESC
        """)

        dados = cursor.fetchall()
        conexao.close()

        for linha in dados:
            id_, ingrediente, qc, vc, qu, unidade, vg = linha

            valores = (
                id_,
                ingrediente,
                self.formatar_numero(qc),
                f"R$ {float(vc or 0):.2f}",
                self.formatar_numero(qu),
                unidade or "",
                f"R$ {float(vg or 0):.2f}"
            )

            self.tabela_fichas.insert("", "end", values=valores)

        self.status_var.set(f"{len(dados)} lançamento(s) na ficha técnica")

    @staticmethod
    def formatar_numero(valor):
        if valor is None:
            return ""

        try:
            numero = float(valor)
            if numero.is_integer():
                return str(int(numero))
            return f"{numero:.2f}"
        except (ValueError, TypeError):
            return str(valor)

    def abrir_popup_ficha(self):
        popup = tk.Toplevel(self)
        popup.title("Novo lançamento - Ficha Técnica")
        popup.geometry("560x600")
        popup.resizable(False, False)
        popup.configure(bg=CORES["branco"])
        popup.transient(self)
        popup.grab_set()

        tk.Label(
            popup,
            text="Novo lançamento",
            font=("Segoe UI", 18, "bold"),
            fg=CORES["texto"],
            bg=CORES["branco"]
        ).pack(anchor="w", padx=30, pady=(25, 4))

        tk.Label(
            popup,
            text="Preencha os dados do ingrediente utilizado.",
            font=("Segoe UI", 9),
            fg=CORES["texto_secundario"],
            bg=CORES["branco"]
        ).pack(anchor="w", padx=30, pady=(0, 18))

        formulario = tk.Frame(popup, bg=CORES["branco"])
        formulario.pack(fill="x", padx=30)

        tk.Label(
            formulario,
            text="Ingrediente",
            font=("Segoe UI", 9, "bold"),
            fg=CORES["texto"],
            bg=CORES["branco"]
        ).pack(anchor="w", pady=(0, 6))

        combo = ttk.Combobox(
            formulario,
            state="readonly",
            font=("Segoe UI", 10)
        )

        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT ingrediente FROM ingredientes ORDER BY ingrediente"
        )
        ingredientes = [linha[0] for linha in cursor.fetchall()]
        conexao.close()

        combo["values"] = ingredientes
        combo.pack(fill="x", ipady=5, pady=(0, 14))

        campos = tk.Frame(formulario, bg=CORES["branco"])
        campos.pack(fill="x")

        campos.columnconfigure(0, weight=1)
        campos.columnconfigure(1, weight=1)

        entry_qtd_comprada = self._campo_grid(
            campos, "Quantidade comprada", 0, 0
        )
        entry_valor_comprado = self._campo_grid(
            campos, "Valor da compra (R$)", 0, 1
        )
        entry_qtd_usada = self._campo_grid(
            campos, "Quantidade usada", 1, 0
        )

        tk.Label(
            campos,
            text="Unidade de medida",
            font=("Segoe UI", 9, "bold"),
            fg=CORES["texto"],
            bg=CORES["branco"]
        ).grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(12, 6))

        combo_unidade = ttk.Combobox(
            campos,
            values=("g", "kg", "ml", "L", "un", "xícara", "colher"),
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_unidade.grid(
            row=2,
            column=1,
            sticky="ew",
            padx=(8, 0),
            ipady=5
        )

        def salvar():
            ingrediente = combo.get().strip()
            unidade = combo_unidade.get().strip()

            try:
                qtd_comprada = float(
                    entry_qtd_comprada.get().replace(",", ".")
                )
                valor_comprado = float(
                    entry_valor_comprado.get().replace(",", ".")
                )
                qtd_usada = float(
                    entry_qtd_usada.get().replace(",", ".")
                )
            except ValueError:
                messagebox.showwarning(
                    "Atenção",
                    "Informe valores numéricos válidos.",
                    parent=popup
                )
                return

            if not ingrediente:
                messagebox.showwarning(
                    "Atenção",
                    "Selecione um ingrediente.",
                    parent=popup
                )
                return

            if not unidade:
                messagebox.showwarning(
                    "Atenção",
                    "Selecione a unidade de medida.",
                    parent=popup
                )
                return

            if qtd_comprada <= 0 or valor_comprado < 0 or qtd_usada <= 0:
                messagebox.showwarning(
                    "Atenção",
                    "As quantidades devem ser maiores que zero e o valor não pode ser negativo.",
                    parent=popup
                )
                return

            if qtd_usada > qtd_comprada:
                messagebox.showwarning(
                    "Atenção",
                    "A quantidade usada não pode ser maior que a quantidade comprada.",
                    parent=popup
                )
                return

            valor_gasto = (qtd_usada / qtd_comprada) * valor_comprado

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO fichas (
                    ingrediente,
                    quantidade_comprada,
                    valor_comprado,
                    quantidade_usada,
                    unidade_medida,
                    valor_gasto
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                ingrediente,
                qtd_comprada,
                valor_comprado,
                qtd_usada,
                unidade,
                valor_gasto
            ))

            conexao.commit()
            conexao.close()

            popup.destroy()
            self.atualizar_tabela_fichas()

            messagebox.showinfo(
                "Lançamento salvo",
                f"Registro salvo com custo utilizado de R$ {valor_gasto:.2f}."
            )

        botoes = tk.Frame(popup, bg=CORES["branco"])
        botoes.pack(fill="x", padx=30, pady=25)

        self.botao(
            botoes,
            "Cancelar",
            popup.destroy,
            "secundario",
            12
        ).pack(side="right")

        self.botao(
            botoes,
            "Salvar lançamento",
            salvar,
            "primario",
            17
        ).pack(side="right", padx=8)

    def _campo_grid(self, parent, label, row, column):
        frame = tk.Frame(parent, bg=CORES["branco"])
        frame.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=(0, 8) if column == 0 else (8, 0),
            pady=(0, 12)
        )

        tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 9, "bold"),
            fg=CORES["texto"],
            bg=CORES["branco"]
        ).pack(anchor="w", pady=(0, 6))

        entry = tk.Entry(
            frame,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            relief="flat",
            highlightthickness=1,
            highlightbackground=CORES["borda"],
            highlightcolor=CORES["primaria"]
        )
        entry.pack(fill="x", ipady=8)

        return entry

    def deletar_ficha(self):
        selecao = self.tabela_fichas.selection()

        if not selecao:
            messagebox.showwarning(
                "Atenção",
                "Selecione um lançamento para excluir."
            )
            return

        if not messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja excluir {len(selecao)} lançamento(s)?"
        ):
            return

        conexao = conectar()
        cursor = conexao.cursor()

        for item in selecao:
            valores = self.tabela_fichas.item(item, "values")
            cursor.execute(
                "DELETE FROM fichas WHERE id = ?",
                (valores[0],)
            )

        conexao.commit()
        conexao.close()

        self.atualizar_tabela_fichas()

        messagebox.showinfo(
            "Sucesso",
            "Lançamento(s) excluído(s) com sucesso."
        )


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    conectar_banco_dados()

    app = FichaTecnicaApp()
    app.mainloop()