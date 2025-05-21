from tkinter import messagebox

import customtkinter as ctk
import sys

from customtkinter import *
from PIL import ImageTk, Image

import modulo_login
from modulo_login import usuarioFunc


# esse módulo login será o arquivo onde ficarão salvos as senhas,
# preciso que alguém faça o banco de dados para eu fazer a verificação de login e senha!!

class LoginFunc(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller


        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frameLogin = ctk.CTkFrame(self, width=300, height=400, fg_color="#78AFE2", border_width=1, border_color="black")
        self.frameLogin.grid(row=0, column=0, sticky="", padx=20, pady=20)
        self.frameLogin.grid_propagate(False)

        self.frameLogin.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=0)
        self.frameLogin.grid_columnconfigure(0, weight=1)

        try:
            self.img_user = Image.open("user_white.png")
            self.img_user_tk = CTkImage(
                light_image=self.img_user,
                dark_image=self.img_user,
                size=(100, 100)
            )
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            self.img_user_tk = None

        ctk.CTkLabel(
            self.frameLogin,
            image=self.img_user_tk,
            text=""
        ).grid(row=0, column=0, pady=(10, 5))

        ctk.CTkLabel(
            self.frameLogin,
            text="Login",
            text_color="white",
            font=('Arial', 45)
        ).grid(row=1, column=0, pady=(0, 15))

        self.e_login = ctk.CTkEntry(self.frameLogin, placeholder_text="Usuário")
        self.e_login.grid(row=2, column=0, padx=20, pady=(0, 10))

        self.e_senha = ctk.CTkEntry(self.frameLogin, placeholder_text="Senha", show="*")
        self.e_senha.grid(row=3, column=0, padx=20, pady=(0, 15))

        self.botaoConfirmar = ctk.CTkButton(
            self.frameLogin,
            text="Confirmar",
            text_color="white",
            font=('Arial', 20),
            bg_color='#13BB99',
            command=self.validar_login_func
        )
        self.botaoConfirmar.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="")

        #Falta arrumar a validação e conectar ela ao botão, para chamar a próxima página
        def validar_login_func(self):
            usuario = self.e_login.get()
            senha = self.e_senha.get()

            if len(usuario) == 0 or len(senha) == 0:
                messagebox.showerror("Erro!", "Login ou senha não podem estar vazios.")
                return

            if usuario == modulo_login.usuarioFunc and senha == modulo_login.senhaFunc:
                messagebox.showinfo("Sucesso!", "Login feito com sucesso.")
                self.controller.mostrar_frame(usuarioFunc)
            else:
                messagebox.showerror("Erro!", "Login ou senha inválidos.")

        
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.state('zoomed')

        self.os_type = sys.platform.lower()
        self.title("Login")

        ctk.set_appearance_mode("light")

        self.bind("<F11>", self.abrir_telacheia)
        self.bind("<Escape>", self.sair_telacheia)


        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Tela in (LoginFunc,):
            frame = Tela(container, self)
            self.frames[Tela] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame(LoginFunc)

    def abrir_telacheia(self, event=None):
        if self.attributes('-fullscreen'):
            self.attributes('-fullscreen', False)
            self.state('zoomed')
        else:
            self.attributes('-fullscreen', True)

    def sair_telacheia(self, event=None):
        self.attributes('-fullscreen', False)
        self.state('zoomed')

    def mostrar_frame(self, tela):
        frame = self.frames[tela]
        frame.tkraise()

if __name__ == '__main__':
    app = App()
    app.mainloop()