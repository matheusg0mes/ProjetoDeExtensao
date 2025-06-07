import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage

import modulo_login
from sistemaSemiFinal.app import JanelaPrincipal


class LoginAdministrativo(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frameLogin = ctk.CTkFrame(self, width=300, height=400, fg_color="#78AFE2", border_width=1, border_color="black")
        self.frameLogin.grid(row=0, column=0, padx=20, pady=20)
        self.frameLogin.grid_propagate(False)

        self.frameLogin.grid_rowconfigure((0,1,2,3,4,5), weight=0)
        self.frameLogin.grid_columnconfigure(0, weight=1)

        try:
            self.img_user = Image.open("user_white.png")
            self.img_user_tk = CTkImage(light_image=self.img_user, dark_image=self.img_user, size=(100,100))
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            self.img_user_tk = None

        ctk.CTkLabel(self.frameLogin, image=self.img_user_tk, text="").grid(row=0, column=0, pady=(10,5))

        ctk.CTkLabel(self.frameLogin, text="Login", text_color="white", font=('Arial', 45)).grid(row=1, column=0, pady=(0,15))

        self.e_login = ctk.CTkEntry(self.frameLogin, placeholder_text="Usuário")
        self.e_login.grid(row=2, column=0, padx=20, pady=(0,10))

        self.e_senha = ctk.CTkEntry(self.frameLogin, placeholder_text="Senha", show="*")
        self.e_senha.grid(row=3, column=0, padx=20, pady=(0,15))

        self.botaoConfirmar = ctk.CTkButton(self.frameLogin, text="Confirmar", text_color="white", font=('Arial', 20), bg_color='#13BB99', command=self.validar_login_func)
        self.botaoConfirmar.grid(row=4, column=0, padx=20, pady=(0,10))

        self.botaoVoltar = ctk.CTkButton(self.frameLogin, text="Voltar", text_color="white", font=('Arial', 20), fg_color='#B22222', hover_color='#B22222', command=self.voltar_principal)
        self.botaoVoltar.grid(row=5, column=0, padx=20, pady=(0,10))

    def validar_login_func(self):
        import sys
        from app import JanelaPrincipal

        usuario = self.e_login.get()
        senha = self.e_senha.get()

        if len(usuario) == 0 or len(senha) == 0:
            messagebox.showerror("Erro!", "Login ou senha não podem estar vazios.")
            return

        if usuario == modulo_login.usuarioAdministrativo and senha == modulo_login.senhaAdministrativo:
            messagebox.showinfo("Sucesso!", "Login feito com sucesso.")
            self.e_login.delete(0, ctk.END)
            self.e_senha.delete(0, ctk.END)
            self.controller.destroy()  # fecha o main.py
            admin_app = JanelaPrincipal()
            admin_app.mainloop()
            sys.exit()
        else:
            messagebox.showerror("Erro!", "Login ou senha inválidos.")

    def voltar_principal(self):
        from janelaPrincipal import Principal
        self.controller.mostrar_frame(Principal)
        self.e_login.delete(0, ctk.END)
        self.e_senha.delete(0, ctk.END)