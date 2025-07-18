import customtkinter as ctk
from cadastro_cliente import JanelaCadastroCliente
from visualizar_cliente import JanelaVisualizarClientes
from cadastro_funcionario import JanelaCadastroFuncionario
from visualizar_funcionario import JanelaVisualizarFuncionarios
from dashboard import JanelaDashboard
from agendar_reuniao import JanelaAgendarReuniao
from cadastro_responsavel import JanelaCadastroResponsavel

# Configurações iniciais
tema_atual = "dark"
ctk.set_appearance_mode(tema_atual)
ctk.set_default_color_theme("dark-blue")

# Cores padrão do sistema
azul_escuro = "#1F6AA5"
azul_claro = "#D6EAF8"
amarelo_escuro = "#000000"
texto_branco = "#FFFFFF"

class JanelaPrincipal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Cadastro")
        self.geometry("1000x600")

        self.tema = "dark"

        # Menu lateral
        self.menu_lateral = ctk.CTkFrame(self, width=200, fg_color=azul_escuro, corner_radius=0)
        self.menu_lateral.pack(side="left", fill="y")

        titulo = ctk.CTkLabel(self.menu_lateral, text="Pestalozzi", font=("Arial", 20), text_color=texto_branco)
        titulo.pack(pady=20)

        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(side="left", fill="both", expand=True)

        self.header = ctk.CTkFrame(self.main_container, height=50, fg_color=amarelo_escuro)
        self.header.pack(fill="x")
        admin_label = ctk.CTkLabel(self.header, text="Administrador", font=("Segoe UI", 22, "bold"), text_color=texto_branco)
        admin_label.pack(side="right", padx=15, pady=10)

        self.botao_tema = ctk.CTkButton(self.header, text="🌙", width=40, command=self.alternar_tema)
        self.botao_tema.pack(side="left", padx=10, pady=5)

        self.main_frame = ctk.CTkFrame(self.main_container)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        self.titulo_aba = ctk.CTkLabel(self.main_frame, text="Cadastrar Cliente", font=("Arial", 18), text_color=texto_branco)
        self.titulo_aba.pack(pady=(10, 20))

        self.conteudo_frame = ctk.CTkFrame(self.main_frame)
        self.conteudo_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.abas = {
            "Dashboard": self.abrir_dashboard,
            "Cadastrar Cliente": self.abrir_cadastro_cliente,
            "Visualizar Cliente": self.abrir_visualizar_cliente,
            "Cadastrar Funcionário": self.abrir_cadastro_funcionario,
            "Visualizar Funcionário": self.abrir_visualizar_funcionario,
            "Agendar Reunião": self.abrir_agendar_reuniao,
            "Cadastrar Responsável": self.abrir_cadastro_responsavel
        }

        for texto, comando in self.abas.items():
            botao = ctk.CTkButton(
                master=self.menu_lateral,
                text=texto,
                command=comando,
                fg_color=azul_claro,
                text_color=azul_escuro,
                hover_color="#AED6F1"
            )
            botao.pack(fill="x", padx=10, pady=5)

        self.abrir_cadastro_cliente()

    def alternar_tema(self):
        self.tema = "light" if self.tema == "dark" else "dark"
        ctk.set_appearance_mode(self.tema)
        self.botao_tema.configure(text="🌞" if self.tema == "dark" else "🌙")

    def abrir_cadastro_cliente(self):
        self.titulo_aba.configure(text="Cadastrar Cliente")
        self.limpar_frame()
        JanelaCadastroCliente(self.conteudo_frame)

    def abrir_visualizar_cliente(self):
        self.titulo_aba.configure(text="Visualizar Cliente")
        self.limpar_frame()
        JanelaVisualizarClientes(self.conteudo_frame)

    def abrir_cadastro_funcionario(self):
        self.titulo_aba.configure(text="Cadastrar Funcionário")
        self.limpar_frame()
        JanelaCadastroFuncionario(self.conteudo_frame)

    def abrir_visualizar_funcionario(self):
        self.titulo_aba.configure(text="Visualizar Funcionário")
        self.limpar_frame()
        JanelaVisualizarFuncionarios(self.conteudo_frame)

    def abrir_dashboard(self):
        self.titulo_aba.configure(text="Dashboard")
        self.limpar_frame()
        JanelaDashboard(self.conteudo_frame)

    def abrir_agendar_reuniao(self):
        self.titulo_aba.configure(text="Agendar Reunião")
        self.limpar_frame()
        JanelaAgendarReuniao(self.conteudo_frame)

    def abrir_cadastro_responsavel(self):
        self.titulo_aba.configure(text="Cadastrar Responsável")
        self.limpar_frame()
        JanelaCadastroResponsavel(self.conteudo_frame)

    def limpar_frame(self):
        for widget in self.conteudo_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()
