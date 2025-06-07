# agendar_reuniao.py
import customtkinter as ctk
from tkinter import messagebox
from conexao_mysql import conectar_mysql
from datetime import datetime

class JanelaAgendarReuniao:
    def __init__(self, parent):
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(expand=True)

        self.vars = {}
        labels = ["Nome da Reunião", "Assunto", "Data (AAAA-MM-DD)", "Conteúdo"]

        for i, label in enumerate(labels):
            ctk.CTkLabel(self.frame, text=label + ":").grid(row=i, column=0, sticky="e", padx=10, pady=10)
            var = ctk.StringVar()
            entry = ctk.CTkEntry(self.frame, textvariable=var, width=400)
            entry.grid(row=i, column=1, sticky="w", padx=10, pady=10)
            self.vars[label] = var

        btn = ctk.CTkButton(self.frame, text="Agendar Reunião", fg_color="green", command=self.agendar)
        btn.grid(row=len(labels), column=0, columnspan=2, pady=20)

    def agendar(self):
        nome = self.vars["Nome da Reunião"].get()
        assunto = self.vars["Assunto"].get()
        data = self.vars["Data (AAAA-MM-DD)"].get()
        conteudo = self.vars["Conteúdo"].get()

        if not all([nome, assunto, data, conteudo]):
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        try:
            datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Data inválida", "Digite a data no formato AAAA-MM-DD.")
            return

        try:
            conn, cursor = conectar_mysql()
            cursor.execute(
                "INSERT INTO reunioes (nome, assunto, data, conteudo) VALUES (%s, %s, %s, %s)",
                (nome, assunto, data, conteudo)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Reunião agendada com sucesso!")
            for var in self.vars.values():
                var.set("")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao agendar reunião: {e}")
