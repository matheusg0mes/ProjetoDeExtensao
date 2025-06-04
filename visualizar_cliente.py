import customtkinter as ctk
from conexao_mysql import conectar_mysql

class JanelaVisualizarClientes:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(expand=True, fill="both")  # preenche tudo

        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.frame, width=1100, height=500, corner_radius=10
        )
        self.scrollable_frame.pack(padx=20, pady=20, expand=True)

        self.colunas = ["Nome", "CPF", "Celular", "Responsável", "Acompanhado por"]
        self.estilos = {
            "header_bg": "#1F6AA5",
            "header_fg": "white",
            "row_bg_1": "#F2F4F4",
            "row_bg_2": "#EAEDED",
            "row_fg": "#1C2833",
        }

        self.criar_cabecalho()
        self.carregar_dados()

    def criar_cabecalho(self):
        for i, coluna in enumerate(self.colunas):
            label = ctk.CTkLabel(
                self.scrollable_frame, text=coluna, width=170, anchor="center",
                font=("Arial", 14, "bold"), text_color=self.estilos["header_fg"],
                fg_color=self.estilos["header_bg"], corner_radius=8
            )
            label.grid(row=0, column=i, padx=2, pady=6, sticky="nsew")

    def carregar_dados(self):
        try:
            conn, cursor = conectar_mysql()
            cursor.execute("SELECT nome, cpf, celular, responsavel, encarregado FROM pessoas")
            dados = cursor.fetchall()
            conn.close()

            for idx, linha in enumerate(dados, start=1):
                cor_fundo = self.estilos["row_bg_1"] if idx % 2 == 0 else self.estilos["row_bg_2"]

                for col, valor in enumerate(linha):
                    ctk.CTkLabel(
                        self.scrollable_frame, text=valor, width=170, anchor="center",
                        font=("Arial", 12), text_color=self.estilos["row_fg"],
                        fg_color=cor_fundo, corner_radius=6
                    ).grid(row=idx, column=col, padx=2, pady=4, sticky="nsew")

        except Exception as e:
            erro_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Erro ao carregar dados: {e}",
                text_color="red"
            )
            erro_label.grid(row=1, column=0, columnspan=len(self.colunas), pady=10)
