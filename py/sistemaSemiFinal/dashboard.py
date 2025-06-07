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
            cursor.execute("SELECT id, nome, assunto, conteudo FROM reunioes WHERE data = %s", (data_hoje,))
            reunioes = cursor.fetchall()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar reuniões: {e}")
            return

        janela = Toplevel(self.parent)
        janela.title("Reuniões de Hoje")
        janela.geometry("650x450")
        janela.grab_set()

        frame = ctk.CTkScrollableFrame(janela)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        if not reunioes:
            ctk.CTkLabel(frame, text="Nenhuma reunião para hoje.", font=("Arial", 14)).pack(pady=20)
            return

        for id_reuniao, nome, assunto, conteudo in reunioes:
            item_frame = ctk.CTkFrame(frame)
            item_frame.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(item_frame, text=f"📌 {nome}", font=("Arial", 16, "bold")).pack(anchor="w")
            ctk.CTkLabel(item_frame, text=f"Assunto: {assunto}", font=("Arial", 14)).pack(anchor="w")
            ctk.CTkLabel(item_frame, text=f"Conteúdo: {conteudo}", font=("Arial", 12), wraplength=500, justify="left").pack(anchor="w", padx=10)

            btn_del = ctk.CTkButton(
                item_frame, text="Deletar", fg_color="red", hover_color="#cc0000",
                command=lambda idr=id_reuniao: self.deletar_reuniao(idr, janela)
            )
            btn_del.pack(anchor="e", pady=5)

    def deletar_reuniao(self, id_reuniao, janela):
        confirmar = messagebox.askyesno("Confirmar", "Deseja deletar esta reunião?")
        if not confirmar:
            return
        try:
            conn, cursor = conectar_mysql()
            cursor.execute("DELETE FROM reunioes WHERE id = %s", (id_reuniao,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Reunião deletada com sucesso!")
            janela.destroy()
            self.exibir_reunioes()
            self.carregar_metricas()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao deletar reunião: {e}")

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
            self.funcionarios_label.pack_forget()
            self.reunioes_label.configure(text=f"📅 Reuniões Hoje: {total_reunioes}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
