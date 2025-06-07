import customtkinter as ctk
from tkinter import messagebox
from conexao_mysql import conectar_mysql, validarcpf
from datetime import datetime

class JanelaCadastroFuncionario:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(expand=True)

        self.entries_vars = {}
        self.var_ativo = ctk.IntVar()

        # Corrigido: sem acento em "Endereco"
        labels = [
            "Nome", "CPF", "Cargo", "Telefone", "Email", "Endereco"
        ]

        for i, label in enumerate(labels):
            row = i // 2
            col = (i % 2) * 2
            ctk.CTkLabel(self.frame, text=label + ":").grid(row=row, column=col, sticky="e", padx=10, pady=10)
            var = ctk.StringVar()
            entry = ctk.CTkEntry(self.frame, textvariable=var, width=400)
            entry.grid(row=row, column=col + 1, sticky="w", padx=10, pady=10)
            self.entries_vars[label] = var

        ctk.CTkLabel(self.frame, text="Ativo:").grid(row=3, column=0, sticky="e", padx=10, pady=10)
        ctk.CTkCheckBox(self.frame, text="Sim", variable=self.var_ativo).grid(row=3, column=1, sticky="w", padx=10, pady=10)

        btn = ctk.CTkButton(self.frame, text="Cadastrar", width=250, fg_color="green", command=self.cadastrar)
        btn.grid(row=4, column=0, columnspan=4, pady=30)

    def cadastrar(self):
        dados = {k: v.get() for k, v in self.entries_vars.items()}
        dados["Ativo"] = "Sim" if self.var_ativo.get() == 1 else "Não"
        dados["DataAdmissao"] = datetime.now().strftime("%Y-%m-%d")

        if not all(dados.values()):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        if not validarcpf(dados["CPF"]):
            messagebox.showwarning("CPF inválido", "Digite um CPF válido.")
            return

        try:
            conn, cursor = conectar_mysql()

            cursor.execute("SELECT cpf FROM funcionarios WHERE cpf = %s", (dados["CPF"],))
            if cursor.fetchone():
                messagebox.showerror("CPF Duplicado", "Já existe um funcionário cadastrado com este CPF.")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO funcionarios (cpf, nome, cargo, telefone, email, endereco, ativo, data_admissao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                dados["CPF"], dados["Nome"], dados["Cargo"], dados["Telefone"],
                dados["Email"], dados["Endereco"], dados["Ativo"], dados["DataAdmissao"]
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")

            for var in self.entries_vars.values():
                var.set("")
            self.var_ativo.set(0)

        except Exception as e:
            print(f"Erro detalhado: {e}")
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")
