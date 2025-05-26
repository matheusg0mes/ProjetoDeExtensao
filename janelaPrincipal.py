import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage

from janelaLoginAdmin import LoginAdministrativo
from janelaLoginFunc import LoginFunc

class Principal(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=0, sticky="nsew")

        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.frame_botoes = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.frame_botoes.grid(row=0, column=0, padx=20, pady=20)

        self.frame_botoes.grid_rowconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)

        try:
            self.img_func = Image.open("imagem_arredondada_com_borda.png")
            self.img_func_tk = CTkImage(
                light_image=self.img_func,
                dark_image=self.img_func,
                size=(400, 350)
            )
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            self.img_func_tk = None

        try:
            self.img_gerencia = Image.open("imagem_gerencia.png")
            self.img_gerencia_tk = CTkImage(
                light_image=self.img_gerencia,
                dark_image=self.img_gerencia,
                size=(400, 350)
            )
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            self.img_gerencia_tk = None

        self.botaoFunc = ctk.CTkButton(
            self.frame_botoes,
            image=self.img_func_tk,
            text="Funcionários",
            text_color='black',
            font=("Arial", 25),
            hover_color="#D3D3D3",
            fg_color="transparent",
            compound="top",
            anchor="center",
            width=500,
            height=500,
            corner_radius=50,
            command=lambda: self.controller.mostrar_frame(LoginFunc)
        )
        self.botaoFunc.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")

        self.botaoGeren = ctk.CTkButton(
            self.frame_botoes,
            image=self.img_gerencia_tk,
            text="Gerenciamento",
            text_color='black',
            font=("Arial", 25),
            hover_color="#D3D3D3",
            fg_color="transparent",
            compound="top",
            anchor="center",
            width=500,
            height=450,
            corner_radius=50,
            command=lambda: self.controller.mostrar_frame(LoginAdministrativo)
        )
        self.botaoGeren.grid(row=0, column=1, padx=40, pady=40, sticky="nsew")
