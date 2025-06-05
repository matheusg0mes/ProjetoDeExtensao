# cadastro_responsavel.py
import customtkinter as ctk
from tkinter import messagebox
from conexao_mysql import conectar_mysql, validarcpf

class JanelaCadastroResponsavel:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(expand=True)

        self.vars = {}
        campos = ["CPF do Responsável", "Nome", "Telefone", "Parentesco", "CPF do Cliente"]

        for i, campo in enumerate(campos):
            ctk.CTkLabel(self.frame, text=campo + ":").grid(row=i, column=0, sticky="e", padx=10, pady=10)
            var = ctk.StringVar()
            entry = ctk.CTkEntry(self.frame, textvariable=var, width=400)
            entry.grid(row=i, column=1, sticky="w", padx=10, pady=10)
            self.vars[campo] = var

        ctk.CTkButton(self.frame, text="Cadastrar", command=self.cadastrar).grid(row=len(campos), column=0, columnspan=2, pady=20)

    def cadastrar(self):
        dados = {campo: var.get().strip() for campo, var in self.vars.items()}

        if not all(dados.values()):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        if not validarcpf(dados["CPF do Responsável"]) or not validarcpf(dados["CPF do Cliente"]):
            return

        try:
            conn, cursor = conectar_mysql()
            cursor.execute("INSERT INTO responsaveis (cpf, nome, telefone, parentesco, cliente_cpf) VALUES (%s, %s, %s, %s, %s)",
                           (dados["CPF do Responsável"], dados["Nome"], dados["Telefone"], dados["Parentesco"], dados["CPF do Cliente"]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Responsável cadastrado com sucesso!")
            for var in self.vars.values():
                var.set("")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar responsável: {e}")
