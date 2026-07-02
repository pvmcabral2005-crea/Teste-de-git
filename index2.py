import tkinter as tk
from tkinter import messagebox

PERGUNTAS = [
    {
        "pergunta": "Qual dia do mês de junho é comemorado São João?",
        "alternativas": [
            "12 de junho",
            "20 de junho",
            "24 de junho",
            "18 de junho"
        ],
        "correta": 2,
        "explicacao":
        "São João é comemorado em 24 de junho, "
        "data que celebra o nascimento de São João Batista."
    },

    {
        "pergunta": "Qual é o alimento mais típico das festas juninas?",
        "alternativas": [
            "Milho",
            "Lasanha",
            "Feijoada",
            "Panelada"
        ],
        "correta": 0,
        "explicacao":
        "O milho é a base de diversas comidas juninas."
    },

    {
        "pergunta": "Qual a principal dança das festas juninas?",
        "alternativas": [
            "Forró",
            "Quadrilha",
            "Salsa",
            "Samba"
        ],
        "correta": 1,
        "explicacao":
        "A quadrilha é a dança tradicional das festas juninas."
    },

    {
        "pergunta":
        "Qual a principal região do Brasil onde os festejos juninos são mais famosos?",

        "alternativas": [
            "Norte",
            "Sudeste",
            "Nordeste",
            "Sul"
        ],

        "correta": 2,

        "explicacao":
        "O Nordeste realiza algumas das maiores festas juninas do mundo."
    },

    {
        "pergunta":
        "Qual destes santos é homenageado nas festas juninas?",

        "alternativas": [
            "São Pedro",
            "São Jorge",
            "Santo Expedito",
            "São Bento"
        ],

        "correta": 0,

        "explicacao":
        "São Pedro é um dos três santos celebrados nas festas juninas."
    },

    {
        "pergunta":
        "Qual destas comidas é tradicionalmente feita com milho?",

        "alternativas": [
            "Sushi",
            "Pamonha",
            "Pizza",
            "Hambúrguer"
        ],

        "correta": 1,

        "explicacao":
        "A pamonha é preparada com milho verde."
    }
]


class QuizArraia:

    def __init__(self):

        self.janela = tk.Tk()

        self.janela.title("Quiz Arraiá do Saber")
        self.janela.geometry("1200x700")
        self.janela.configure(bg="#F5DEB3")

        self.pontos = 0
        self.indice = 0

        self.criar_tela_inicial()

        self.janela.mainloop()



    def limpar(self):
        for widget in self.janela.winfo_children():
            widget.destroy()

    

    def criar_tela_inicial(self):

        self.limpar()

        titulo = tk.Label(
            self.janela,
            text="🎉 QUIZ ARRAIÁ DO SABER 🎉",
            font=("Arial", 28, "bold"),
            bg="#F5DEB3",
            fg="#8B4513"
        )

        titulo.pack(pady=60)

        subtitulo = tk.Label(
            self.janela,
            text="Teste seus conhecimentos sobre as festas juninas",
            font=("Arial", 16),
            bg="#F5DEB3"
        )

        subtitulo.pack()

        tk.Button(
            self.janela,
            text="INICIAR QUIZ",
            font=("Arial", 16),
            width=20,
            bg="#E67E22",
            command=self.iniciar
        ).pack(pady=30)

        tk.Button(
            self.janela,
            text="INSTRUÇÕES",
            font=("Arial", 16),
            width=20,
            bg="#F1C40F",
            command=self.instrucoes
        ).pack(pady=10)

        tk.Button(
            self.janela,
            text="SAIR",
            font=("Arial", 16),
            width=20,
            bg="#C0392B",
            fg="white",
            command=self.janela.destroy
        ).pack(pady=10)

    

    def instrucoes(self):

        messagebox.showinfo(
            "Instruções",
            "Escolha a alternativa correta\n"
            "e clique em Confirmar."
        )


    def iniciar(self):

        self.pontos = 0
        self.indice = 0

        self.mostrar_pergunta()


    def mostrar_pergunta(self):

        self.limpar()

        pergunta = PERGUNTAS[self.indice]

        tk.Label(
            self.janela,
            text=f"Pergunta {self.indice+1} de {len(PERGUNTAS)}",
            font=("Arial", 16, "bold"),
            bg="#F5DEB3"
        ).pack(pady=10)

       
        progresso = int(
            ((self.indice+1)/len(PERGUNTAS))*100
        )

        tk.Label(
            self.janela,
            text=f"Progresso: {progresso}%",
            font=("Arial", 12),
            bg="#F5DEB3"
        ).pack()

        tk.Label(
            self.janela,
            text=f"Pontos: {self.pontos}",
            font=("Arial", 14),
            bg="#F5DEB3"
        ).pack(pady=10)

        tk.Label(
            self.janela,
            text=pergunta["pergunta"],
            font=("Arial", 20, "bold"),
            bg="#F5DEB3",
            wraplength=1000
        ).pack(pady=40)

        self.resposta = tk.IntVar()
        self.resposta.set(-1)

        for i, alternativa in enumerate(
                pergunta["alternativas"]):

            tk.Radiobutton(
                self.janela,
                text=alternativa,
                variable=self.resposta,
                value=i,
                font=("Arial", 16),
                bg="#F5DEB3"
            ).pack(anchor="center", pady=10)

        tk.Button(
            self.janela,
            text="CONFIRMAR",
            font=("Arial", 16),
            width=20,
            bg="#E67E22",
            command=self.verificar
        ).pack(pady=40)

    def verificar(self):

        escolha = self.resposta.get()

        if escolha == -1:
            messagebox.showwarning(
                "Aviso",
                "Selecione uma resposta."
            )
            return

        pergunta = PERGUNTAS[self.indice]

        if escolha == pergunta["correta"]:

            self.pontos += 1

            messagebox.showinfo(
                "✅ Correto",
                pergunta["explicacao"]
            )

        else:

            correta = pergunta["alternativas"][
                pergunta["correta"]
            ]

            messagebox.showerror(
                "❌ Incorreto",
                f"Resposta correta:\n{correta}\n\n"
                f"{pergunta['explicacao']}"
            )

        self.indice += 1

        if self.indice < len(PERGUNTAS):
            self.mostrar_pergunta()
        else:
            self.resultado()

    

    def classificacao(self):

        if self.pontos == 6:
            return "🏆 Mestre do Arraiá"

        elif self.pontos >= 4:
            return "🥈 Especialista Junino"

        elif self.pontos >= 2:
            return "🥉 Aprendiz Junino"

        return "🎪 Visitante do Arraiá"

    

    def resultado(self):

        self.limpar()

        percentual = int(
            self.pontos/len(PERGUNTAS)*100
        )

        tk.Label(
            self.janela,
            text="RESULTADO FINAL",
            font=("Arial", 28, "bold"),
            bg="#F5DEB3",
            fg="#8B4513"
        ).pack(pady=40)

        tk.Label(
            self.janela,
            text=f"Pontuação: {self.pontos}/6",
            font=("Arial", 22),
            bg="#F5DEB3"
        ).pack()

        tk.Label(
            self.janela,
            text=f"Aproveitamento: {percentual}%",
            font=("Arial", 20),
            bg="#F5DEB3"
        ).pack(pady=20)

        tk.Label(
            self.janela,
            text=self.classificacao(),
            font=("Arial", 24, "bold"),
            bg="#F5DEB3"
        ).pack(pady=20)

        tk.Button(
            self.janela,
            text="JOGAR NOVAMENTE",
            font=("Arial", 16),
            width=20,
            bg="#E67E22",
            command=self.iniciar
        ).pack(pady=20)

        tk.Button(
            self.janela,
            text="MENU",
            font=("Arial", 16),
            width=20,
            bg="#F1C40F",
            command=self.criar_tela_inicial
        ).pack(pady=10)

        tk.Button(
            self.janela,
            text="SAIR",
            font=("Arial", 16),
            width=20,
            bg="#C0392B",
            fg="white",
            command=self.janela.destroy
        ).pack(pady=10)

QuizArraia()