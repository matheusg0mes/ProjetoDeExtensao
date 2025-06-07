import customtkinter as ctk
from tkinter import messagebox
from conexao_mysql import conectar_mysql, validarcpf

class JanelaCadastroCliente:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(expand=True)

        self.entries_vars = {}
        self.var_atendido = ctk.IntVar()

        labels = [
            "Nome", "CPF", "Celular", "Responsável", "Endereço",
            "Frequência", "Escolaridade", "Restrição",
            "Acompanhado por", "Sexo"
        ]

        for i, label in enumerate(labels):
            row = i // 2
            col = (i % 2) * 2
            ctk.CTkLabel(self.frame, text=label + ":").grid(row=row, column=col, sticky="e", padx=10, pady=10)
            var = ctk.StringVar()
            entry = ctk.CTkEntry(self.frame, textvariable=var, width=400)
            entry.grid(row=row, column=col + 1, sticky="w", padx=10, pady=10)
            self.entries_vars[label] = var

        ctk.CTkLabel(self.frame, text="Atendido:").grid(row=5, column=0, sticky="e", padx=10, pady=10)
        ctk.CTkCheckBox(self.frame, text="Sim", variable=self.var_atendido).grid(row=5, column=1, sticky="w", padx=10, pady=10)

        btn = ctk.CTkButton(self.frame, text="Cadastrar", width=250, fg_color="green", command=self.cadastrar)
        btn.grid(row=6, column=0, columnspan=4, pady=30)

    def cadastrar(self):
        dados = {k: v.get() for k, v in self.entries_vars.items()}
        dados["Atendido"] = "Sim" if self.var_atendido.get() == 1 else "Não"

        if not all(dados.values()):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        if not validarcpf(dados["CPF"]):
            return

        try:
            conn, cursor = conectar_mysql()

            cursor.execute("SELECT id FROM pessoas WHERE cpf = %s", (dados["CPF"],))
            if cursor.fetchone():
                messagebox.showerror("CPF Duplicado", "Já existe um cliente cadastrado com este CPF.")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO pessoas (nome, cpf, celular, responsavel, endereco, frequencia,
                                     escolaridade, atendido, restricao, encarregado, sexo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                dados["Nome"], dados["CPF"], dados["Celular"], dados["Responsável"],
                dados["Endereço"], dados["Frequência"], dados["Escolaridade"],
                dados["Atendido"], dados["Restrição"], dados["Acompanhado por"], dados["Sexo"]
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

            for var in self.entries_vars.values():
                var.set("[limpo]")  # para forçar alteração mínima e atualizar
            self.var_atendido.set(0)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")
