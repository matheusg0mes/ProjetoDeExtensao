from tkinter import *
from PIL import Image, ImageTk


class Principal(Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller


        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frameBotoes = Frame(self)
        self.frameBotoes.grid(row=0, column=0, sticky="nsew")


        self.frameBotoes.grid_rowconfigure(0, weight=1)
        self.frameBotoes.grid_columnconfigure(0, weight=1)
        self.frameBotoes.grid_columnconfigure(1, weight=1)


        try:
            self.img_func = Image.open("imagem_arredondada_com_borda.png")
            self.img_func = self.img_func.resize((380, 380))
            self.img_func_tk = ImageTk.PhotoImage(self.img_func)
        except:

            self.img_func_tk = None


        try:
            self.img_gerencia = Image.open("imagem_gerencia_editada.png")
            self.img_gerencia = self.img_gerencia.resize((380, 380))
            self.img_gerencia_tk = ImageTk.PhotoImage(self.img_gerencia)
        except:

            self.img_gerencia_tk = None


        self.frameFunc = Frame(self.frameBotoes)
        self.frameFunc.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.botaoFuncionarios = Button(
            self.frameFunc,
            image=self.img_func_tk,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.botaoFuncionarios.pack(expand=True)
        Label(self.frameFunc, text='Funcionários').pack(pady=5)


        self.frameGerencia = Frame(self.frameBotoes)
        self.frameGerencia.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.botaoGerencia = Button(
            self.frameGerencia,
            image=self.img_gerencia_tk,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.botaoGerencia.pack(expand=True)
        Label(self.frameGerencia, text='Administrativo').pack(pady=5)


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.title("Janela Principal")

        container = Frame(self)
        container.pack(fill="both", expand=True)


        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for Tela in (Principal,):
            frame = Tela(container, self)
            self.frames[Tela] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame(Principal)

    def mostrar_frame(self, tela):
        frame = self.frames[tela]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()