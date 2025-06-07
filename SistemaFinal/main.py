import customtkinter as ctk
import sys

from janelaLoginAdmin import LoginAdministrativo
from janelaLoginFunc import LoginFunc
from janelaPrincipal import Principal

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.attributes("-fullscreen", True)
        self.title("Início")

        ctk.set_appearance_mode("light")

        self.bind("<F11>", self.abrir_telacheia)
        self.bind("<Escape>", self.sair_telacheia)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Tela in (Principal, LoginFunc, LoginAdministrativo):
            frame = Tela(container, self)
            self.frames[Tela] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame(Principal)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()