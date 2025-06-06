# dashboard.py
import customtkinter as ctk
from tkinter import messagebox, Toplevel
from conexao_mysql import conectar_mysql
from datetime import datetime

class JanelaDashboard:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ctk.CTkFrame(parent)
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.titulo = ctk.CTkLabel(self.frame, text="📊 Dashboard", font=("Arial", 22, "bold"))
        self.titulo.pack(pady=10)

        self.metricas_frame = ctk.CTkFrame(self.frame)
        self.metricas_frame.pack(pady=20)

        self.clientes_label = ctk.CTkLabel(self.metricas_frame, text="", font=("Arial", 18))
        self.funcionarios_label = ctk.CTkLabel(self.metricas_frame, text="", font=("Arial", 18))
        self.reunioes_label = ctk.CTkLabel(self.metricas_frame, text="", font=("Arial", 18))

        self.clientes_label.grid(row=0, column=0, padx=40, pady=10)
        self.funcionarios_label.grid(row=0, column=1, padx=40, pady=10)
        self.reunioes_label.grid(row=0, column=2, padx=40, pady=10)

        self.botao_ver_reunioes = ctk.CTkButton(
            self.frame, text="📅 Ver Reuniões de Hoje", command=self.exibir_reunioes
        )
        self.botao_ver_reunioes.pack(pady=10)

        self.carregar_metricas()

    def carregar_metricas(self):
        try:
            conn, cursor = conectar_mysql()
            cursor.execute("SELECT COUNT(*) FROM pessoas")
            total_clientes = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM funcionarios")
            total_funcionarios = cursor.fetchone()[0]
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT COUNT(*) FROM reunioes WHERE data = %s", (data_hoje,))
            total_reunioes = cursor.fetchone()[0]
            conn.close()

            self.clientes_label.configure(text=f"👥 Clientes: {total_clientes}")
            self.funcionarios_label.configure(text=f"🧑‍💼 Funcionários: {total_funcionarios}")
            self.reunioes_label.configure(text=f"📅 Reuniões Hoje: {total_reunioes}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")

    def exibir_reunioes(self):
        try:
            conn, cursor = conectar_mysql()
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT nome, assunto, conteudo FROM reunioes WHERE data = %s", (data_hoje,))
            reunioes = cursor.fetchall()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar reuniões: {e}")
            return

        janela = Toplevel(self.parent)
        janela.title("Reuniões de Hoje")
        janela.geometry("600x400")
        janela.grab_set()

        frame = ctk.CTkScrollableFrame(janela)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        if not reunioes:
            ctk.CTkLabel(frame, text="Nenhuma reunião para hoje.", font=("Arial", 14)).pack(pady=20)
            return

        for nome, assunto, conteudo in reunioes:
            ctk.CTkLabel(frame, text=f"📌 {nome}", font=("Arial", 16, "bold")).pack(anchor="w", pady=5)
            ctk.CTkLabel(frame, text=f"Assunto: {assunto}", font=("Arial", 14)).pack(anchor="w")
            ctk.CTkLabel(frame, text=f"Conteúdo: {conteudo}", font=("Arial", 12), wraplength=550, justify="left").pack(anchor="w", padx=10, pady=(0, 10))

class JanelaDashboardFuncionario(JanelaDashboard):
    def carregar_metricas(self):
        try:
            conn, cursor = conectar_mysql()
            cursor.execute("SELECT COUNT(*) FROM pessoas")
            total_clientes = cursor.fetchone()[0]
            data_hoje = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("SELECT COUNT(*) FROM reunioes WHERE data = %s", (data_hoje,))
            total_reunioes = cursor.fetchone()[0]
            conn.close()

            self.clientes_label.configure(text=f"👥 Clientes: {total_clientes}")
            self.funcionarios_label.pack_forget()  # Oculta o label de funcionários
            self.reunioes_label.configure(text=f"📅 Reuniões Hoje: {total_reunioes}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
