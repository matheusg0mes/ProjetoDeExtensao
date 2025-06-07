import customtkinter as ctk
from tkinter import messagebox, Toplevel, StringVar
from conexao_mysql import conectar_mysql

class JanelaVisualizarClientes:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(expand=True, fill="both")

        self.busca_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.busca_frame.pack(fill="x", padx=20, pady=(10, 0))

        self.cpf_var = StringVar()
        self.entrada_cpf = ctk.CTkEntry(
            self.busca_frame,
            placeholder_text="Digite o CPF do cliente (000.000.000-00)",
            textvariable=self.cpf_var,
            width=300
        )
        self.entrada_cpf.pack(side="left", padx=(0, 10))

        self.botao_buscar = ctk.CTkButton(
            self.busca_frame,
            text="Buscar",
            command=self.buscar_cliente_por_cpf
        )
        self.botao_buscar.pack(side="left")

        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.frame, width=1200, height=500, corner_radius=10
        )
        self.scrollable_frame.pack(padx=20, pady=20, expand=True)

        self.colunas = ["Nome", "CPF", "Celular", "Responsável", "Acompanhado por", "", "", ""]
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
            if coluna.strip():
                label = ctk.CTkLabel(
                    self.scrollable_frame, text=coluna, width=150, anchor="center",
                    font=("Arial", 14, "bold"), text_color=self.estilos["header_fg"],
                    fg_color=self.estilos["header_bg"], corner_radius=8
                )
            else:
                label = ctk.CTkLabel(
                    self.scrollable_frame, text="", width=150, anchor="center",
                    font=("Arial", 14), fg_color="transparent"
                )
            label.grid(row=0, column=i, padx=2, pady=6, sticky="nsew")

    def carregar_dados(self):
        for widget in self.scrollable_frame.winfo_children():
            if int(widget.grid_info().get("row", 1)) > 0:
                widget.destroy()

        try:
            conn, cursor = conectar_mysql()
            cursor.execute("SELECT nome, cpf, celular, responsavel, encarregado FROM pessoas")
            dados = cursor.fetchall()
            conn.close()

            for idx, linha in enumerate(dados, start=1):
                cor_fundo = self.estilos["row_bg_1"] if idx % 2 == 0 else self.estilos["row_bg_2"]

                for col, valor in enumerate(linha):
                    ctk.CTkLabel(
                        self.scrollable_frame, text=str(valor), width=150, anchor="center",
                        font=("Arial", 12), text_color=self.estilos["row_fg"],
                        fg_color=cor_fundo, corner_radius=6
                    ).grid(row=idx, column=col, padx=2, pady=4, sticky="nsew")

                botoes_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
                botoes_frame.grid(row=idx, column=len(self.colunas) - 3, columnspan=3, sticky="w", padx=0)

                ctk.CTkButton(
                    botoes_frame, text="Ver", width=55,
                    command=lambda cpf=linha[1]: self.ver_responsavel_do_cliente(cpf)
                ).pack(side="left", padx=(0, 4))

                ctk.CTkButton(
                    botoes_frame, text="Editar", width=55,
                    command=lambda c=linha[1]: self.abrir_janela_alterar(c)
                ).pack(side="left", padx=(0, 4))

                ctk.CTkButton(
                    botoes_frame, text="X", width=35, fg_color="red",
                    hover_color="#cc0000",
                    command=lambda c=linha[1]: self.confirmar_deletar(c)
                ).pack(side="left", padx=(0, 4))

        except Exception as e:
            erro_label = ctk.CTkLabel(
                self.scrollable_frame,
                text=f"Erro ao carregar dados: {e}",
                text_color="red"
            )
            erro_label.grid(row=1, column=0, columnspan=len(self.colunas), pady=10)



    def ver_responsavel_do_cliente(self, cpf_cliente):
        try:
            conn, cursor = conectar_mysql()
            cursor.execute("SELECT nome, telefone, parentesco FROM responsaveis WHERE cliente_cpf = %s", (cpf_cliente,))
            dados = cursor.fetchone()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar responsável: {e}")
            return

        if not dados:
            messagebox.showinfo("Não encontrado", "Nenhum responsável cadastrado para este cliente.")
            return

        janela = Toplevel(self.parent)
        janela.title(f"Responsável do Cliente - CPF: {cpf_cliente}")
        janela.geometry("500x400")
        janela.grab_set()

        frame = ctk.CTkScrollableFrame(janela, width=480, height=380)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(
            frame, text="👨‍👩‍👧 Dados do Responsável", font=("Arial", 20, "bold"),
            anchor="center", justify="center"
        ).grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        campos = ["Nome", "Telefone", "Parentesco"]
        for i, campo in enumerate(campos, start=1):
            ctk.CTkLabel(
                frame, text=f"{campo}:", font=("Arial", 14, "bold"),
                anchor="center", width=200
            ).grid(row=i, column=0, padx=10, pady=10, sticky="e")

            ctk.CTkLabel(
                frame, text=dados[i - 1], font=("Arial", 14),
                anchor="center", width=250
            ).grid(row=i, column=1, padx=10, pady=10, sticky="w")




    def confirmar_deletar(self, cpf):
        resposta = messagebox.askyesno("Confirmar exclusão", f"Tem certeza que deseja deletar o cliente com CPF {cpf}?")
        if resposta:
            self.deletar_cliente(cpf)

    def deletar_cliente(self, cpf):
        try:
            conn, cursor = conectar_mysql()
            cursor.execute("DELETE FROM pessoas WHERE cpf = %s", (cpf,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!")
            self.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar cliente: {e}")

    def abrir_janela_alterar(self, cpf):
        try:
            conn, cursor = conectar_mysql()
            cursor.execute("SELECT nome, celular, responsavel, encarregado FROM pessoas WHERE cpf = %s", (cpf,))
            dados = cursor.fetchone()
            conn.close()
            if not dados:
                messagebox.showerror("Erro", "Cliente não encontrado.")
                return
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados: {e}")
            return

        janela = Toplevel(self.parent)
        janela.title(f"Alterar Cliente - CPF: {cpf}")
        janela.geometry("400x300")
        janela.grab_set()

        labels = ["Nome", "Celular", "Responsável", "Acompanhado por"]
        vars = {}

        for i, label in enumerate(labels):
            ctk.CTkLabel(janela, text=label+":").grid(row=i, column=0, sticky="e", padx=10, pady=10)
            var = StringVar(value=dados[i])
            entry = ctk.CTkEntry(janela, textvariable=var, width=250)
            entry.grid(row=i, column=1, sticky="w", padx=10, pady=10)
            vars[label] = var

        def salvar_alteracoes():
            novo_nome = vars["Nome"].get()
            novo_celular = vars["Celular"].get()
            novo_responsavel = vars["Responsável"].get()
            novo_acompanhado = vars["Acompanhado por"].get()

            if not (novo_nome and novo_celular and novo_responsavel and novo_acompanhado):
                messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
                return

            try:
                conn, cursor = conectar_mysql()
                cursor.execute("""
                    UPDATE pessoas SET nome=%s, celular=%s, responsavel=%s, encarregado=%s WHERE cpf=%s
                """, (novo_nome, novo_celular, novo_responsavel, novo_acompanhado, cpf))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                janela.destroy()
                self.carregar_dados()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar cliente: {e}")

        btn_salvar = ctk.CTkButton(janela, text="Salvar", command=salvar_alteracoes)
        btn_salvar.grid(row=len(labels), column=0, columnspan=2, pady=20, padx=20, sticky="ew")



    def exibir_detalhes_cliente(self, cliente):
        janela = Toplevel(self.parent)
        janela.title(f"Detalhes do Cliente - CPF: {cliente[1]}")
        janela.geometry("600x600")
        janela.grab_set()

        frame = ctk.CTkScrollableFrame(janela, width=580, height=580)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        labels = [
            "Nome", "CPF", "Celular", "Responsável", "Endereço",
            "Frequência", "Escolaridade", "Atendido", "Restrição",
            "Acompanhado por", "Sexo"
        ]

        ctk.CTkLabel(
            frame, text="📄 Dados do Cliente", font=("Arial", 20, "bold"),
            anchor="center", justify="center"
        ).grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        for i, campo in enumerate(labels, start=1):
            ctk.CTkLabel(
                frame, text=f"{campo}:", font=("Arial", 14, "bold"),
                anchor="center", width=200
            ).grid(row=i, column=0, padx=10, pady=8, sticky="e")

            ctk.CTkLabel(
                frame, text=cliente[i - 1], font=("Arial", 14),
                anchor="center", width=300
            ).grid(row=i, column=1, padx=10, pady=8, sticky="w")

        # Adicionar detalhes do responsável
        try:
            conn, cursor = conectar_mysql()
            cursor.execute("SELECT nome, telefone, parentesco FROM responsaveis WHERE cliente_cpf = %s", (cliente[1],))
            responsavel = cursor.fetchone()
            conn.close()
        except Exception as e:
            responsavel = None
            print(f"Erro ao buscar responsável: {e}")

        if responsavel:
            ctk.CTkLabel(frame, text="👨‍👩‍👧 Responsável pelo Cliente", font=("Arial", 16, "bold")).grid(row=13,
                                                                                                        column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=(20, 10))
            campos_resp = ["Nome", "Telefone", "Parentesco"]
            for i, dado in enumerate(responsavel, start=14):
                ctk.CTkLabel(frame, text=f"{campos_resp[i - 14]}:", font=("Arial", 14, "bold")).grid(row=i, column=0,
                                                                                                     padx=10, pady=5,
                                                                                                     sticky="e")
                ctk.CTkLabel(frame, text=dado, font=("Arial", 14)).grid(row=i, column=1, padx=10, pady=5, sticky="w")

    def buscar_cliente_por_cpf(self):
        cpf = self.cpf_var.get().strip()
        if not cpf:
            messagebox.showwarning("CPF vazio", "Por favor, digite um CPF.")
            return

        try:
            conn, cursor = conectar_mysql()
            cursor.execute("""
                           SELECT nome,
                                  cpf,
                                  celular,
                                  responsavel,
                                  endereco,
                                  frequencia,
                                  escolaridade,
                                  atendido,
                                  restricao,
                                  encarregado,
                                  sexo
                           FROM pessoas
                           WHERE cpf = %s
                           """, (cpf,))
            cliente = cursor.fetchone()
            conn.close()

            if not cliente:
                messagebox.showinfo("Não encontrado", f"Nenhum cliente com o CPF {cpf} foi encontrado.")
                return

            self.exibir_detalhes_cliente(cliente)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar cliente: {e}")
