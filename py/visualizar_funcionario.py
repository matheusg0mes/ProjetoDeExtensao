import customtkinter as ctk
from tkinter import messagebox, Toplevel, StringVar
from conexao_mysql import conectar_mysql

class JanelaVisualizarFuncionarios:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(expand=True, fill="both")

        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.frame, width=1100, height=500, corner_radius=10
        )
        self.scrollable_frame.pack(padx=20, pady=20, expand=True)

        self.colunas = ["CPF", "Nome", "Cargo", "Telefone", "Email", "Data de Admissão", "Alterar", "Deletar"]
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
                self.scrollable_frame, text=coluna, width=130, anchor="center",
                font=("Arial", 14, "bold"), text_color=self.estilos["header_fg"],
                fg_color=self.estilos["header_bg"], corner_radius=8
            )
            label.grid(row=0, column=i, padx=2, pady=6, sticky="nsew")

    def carregar_dados(self):
        # Limpa os widgets anteriores (se recarregar)
        for widget in self.scrollable_frame.winfo_children():
            if int(widget.grid_info().get("row", 1)) > 0:  # Remove só linhas de dados
                widget.destroy()

        try:
            conn, cursor = conectar_mysql()
            cursor.execute("""
                SELECT cpf, nome, cargo, telefone, email, data_admissao FROM funcionarios
            """)
            dados = cursor.fetchall()
            conn.close()

            for idx, linha in enumerate(dados, start=1):
                cor_fundo = self.estilos["row_bg_1"] if idx % 2 == 0 else self.estilos["row_bg_2"]

                for col, valor in enumerate(linha):
                    ctk.CTkLabel(
                        self.scrollable_frame, text=str(valor), width=130, anchor="center",
                        font=("Arial", 12), text_color=self.estilos["row_fg"],
                        fg_color=cor_fundo, corner_radius=6
                    ).grid(row=idx, column=col, padx=2, pady=4, sticky="nsew")

                # Botão Alterar
                btn_alterar = ctk.CTkButton(
                    self.scrollable_frame, text="Alterar", width=80,
                    command=lambda c=linha[0]: self.abrir_janela_alterar(c)
                )
                btn_alterar.grid(row=idx, column=len(self.colunas) - 2, padx=5, pady=4)

                # Botão Deletar
                btn_deletar = ctk.CTkButton(
                    self.scrollable_frame, text="Deletar", width=80, fg_color="red",
                    hover_color="#cc0000",
                    command=lambda c=linha[0]: self.confirmar_deletar(c)
                )
                btn_deletar.grid(row=idx, column=len(self.colunas) - 1, padx=5, pady=4)

        except Exception as e:
            erro_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Erro ao carregar dados: {e}",
                text_color="red"
            )
            erro_label.grid(row=1, column=0, columnspan=len(self.colunas), pady=10)

    def confirmar_deletar(self, cpf):
        resposta = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja deletar o funcionário com CPF {cpf}?")
        if resposta:
            self.deletar_funcionario(cpf)

    def deletar_funcionario(self, cpf):
        try:
            conn, cursor = conectar_mysql()
            cursor.execute("DELETE FROM funcionarios WHERE cpf = %s", (cpf,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Funcionário deletado com sucesso!")
            self.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar funcionário: {e}")

    def abrir_janela_alterar(self, cpf):
        # Busca dados atuais do funcionário
        try:
            conn, cursor = conectar_mysql()
            cursor.execute("SELECT nome, cargo, telefone, email FROM funcionarios WHERE cpf = %s", (cpf,))
            dados = cursor.fetchone()
            conn.close()
            if not dados:
                messagebox.showerror("Erro", "Funcionário não encontrado.")
                return
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados: {e}")
            return

        # Cria a janela de edição
        janela = Toplevel(self.parent)
        janela.title(f"Alterar Funcionário - CPF: {cpf}")
        janela.geometry("400x300")
        janela.grab_set()  # Modal

        labels = ["Nome", "Cargo", "Telefone", "Email"]
        vars = {}

        for i, label in enumerate(labels):
            ctk.CTkLabel(janela, text=label+":").grid(row=i, column=0, sticky="e", padx=10, pady=10)
            var = StringVar(value=dados[i])
            entry = ctk.CTkEntry(janela, textvariable=var, width=250)
            entry.grid(row=i, column=1, sticky="w", padx=10, pady=10)
            vars[label] = var

        def salvar_alteracoes():
            novo_nome = vars["Nome"].get()
            novo_cargo = vars["Cargo"].get()
            novo_telefone = vars["Telefone"].get()
            novo_email = vars["Email"].get()

            if not (novo_nome and novo_cargo and novo_telefone and novo_email):
                messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
                return

            try:
                conn, cursor = conectar_mysql()
                cursor.execute("""
                    UPDATE funcionarios SET nome=%s, cargo=%s, telefone=%s, email=%s WHERE cpf=%s
                """, (novo_nome, novo_cargo, novo_telefone, novo_email, cpf))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
                janela.destroy()
                self.carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar funcionário: {e}")

        btn_salvar = ctk.CTkButton(janela, text="Salvar", command=salvar_alteracoes)
        btn_salvar.grid(row=len(labels), column=0, columnspan=2, pady=20, padx=20, sticky="ew")

