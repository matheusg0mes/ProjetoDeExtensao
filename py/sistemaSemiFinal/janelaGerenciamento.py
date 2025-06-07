import customtkinter as ctk
from PIL import Image
from customtkinter import *


class TelaGerenciamento(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        try:
            self.img_seta = CTkImage(Image.open("seta.png"), size=(20, 20))
            self.img_btn_gerenciamento = CTkImage(Image.open("img_gerenciamento.png"), size=(50, 50))
            self.img_btn_cadastro = CTkImage(Image.open("img_cadastro.png"), size=(50, 50))
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")
            self.img_seta = self.img_btn_gerenciamento = self.img_btn_cadastro = None


        self.fonte_normal = CTkFont(family="Arial", size=25, underline=False)
        self.fonte_sublinhada = CTkFont(family="Arial", size=25, underline=True)

        self.mainFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.mainFrame.grid(row=0, column=0, sticky="nsew")
        self.mainFrame.grid_columnconfigure(0, weight=0)
        self.mainFrame.grid_columnconfigure(1, weight=1)
        self.mainFrame.grid_rowconfigure(0, weight=1)

        self.frameBotoes = ctk.CTkFrame(self.mainFrame, fg_color="#0B5FAE", width=300, corner_radius=0)
        self.frameBotoes.grid(row=0, column=0, sticky="ns")
        self.frameBotoes.grid_propagate(False)

        # Botão voltar
        self.botaoVoltar = CTkButton(self.frameBotoes, text="Sair",
                                     image=self.img_seta,
                                     fg_color="transparent",
                                     text_color="white",
                                     font=self.fonte_normal,
                                     hover=False,
                                     command=self.voltar,
                                     height=40, width=200)
        self.botaoVoltar.grid(sticky="ew", padx=10, pady=10)
        self.botaoVoltar.bind("<Enter>", self.sublinhar)
        self.botaoVoltar.bind("<Leave>", self.tirar_sublinhado)


        self.linha_cima = ctk.CTkFrame(self.frameBotoes, height=2, fg_color="white")
        self.linha_cima.grid(sticky="ew", padx=0, pady=(100, 10))


        self.botaoGerenciamento = CTkButton(self.frameBotoes,
                                            text="Gerenciamento",
                                            image=self.img_btn_gerenciamento,
                                            fg_color="transparent",
                                            text_color="white",
                                            font=self.fonte_normal,
                                            hover=False,
                                            height=40, width=200)
        self.botaoGerenciamento.grid(sticky="ew", padx= 30, pady=(0, 5))
        self.botaoGerenciamento.bind("<Enter>", self.sublinhar)
        self.botaoGerenciamento.bind("<Leave>", self.tirar_sublinhado)


        self.linha_meio = ctk.CTkFrame(self.frameBotoes, height=2, fg_color="white")
        self.linha_meio.grid(sticky="ew", padx=0, pady=(4, 4))


        self.botaoCadastro = CTkButton(self.frameBotoes,
                                       text="Cadastro",
                                       image=self.img_btn_cadastro,
                                       fg_color="transparent",
                                       text_color="white",
                                       font=self.fonte_normal,
                                       hover=False,
                                       height=40, width=200)
        self.botaoCadastro.grid(sticky="ew", padx=30, pady=(5, 0))
        self.botaoCadastro.bind("<Enter>", self.sublinhar)
        self.botaoCadastro.bind("<Leave>", self.tirar_sublinhado)


        self.linha_baixo = ctk.CTkFrame(self.frameBotoes, height=2, fg_color="white")
        self.linha_baixo.grid(sticky="ew", padx=0, pady=(5, 10))


        self.framePrincipal = ctk.CTkFrame(self.mainFrame, fg_color="#F2F2F2", corner_radius=0)
        self.framePrincipal.grid(row=0, column=1, sticky="nsew")

        frame_topo = ctk.CTkFrame(self.framePrincipal, fg_color="transparent")
        frame_topo.grid(row=0, column=0, padx=50, pady=40, sticky="w")

        label_principal = ctk.CTkLabel(frame_topo,
                                       text="Gerenciamento",
                                       text_color="black",
                                       font=ctk.CTkFont(size=25, weight="bold"))
        label_principal.pack(side="left")

        label_secundario = ctk.CTkLabel(frame_topo,
                                        text="clientes cadastrados",
                                        text_color="gray",
                                        font=ctk.CTkFont(size=15, weight="normal"))
        label_secundario.pack(side="left", padx=(6, 0), pady=(6,0))

    def sublinhar(self, event):
        event.widget.configure(font=self.fonte_sublinhada)

    def tirar_sublinhado(self, event):
        event.widget.configure(font=self.fonte_normal)

    def voltar(self):
        from janelaPrincipal import Principal
        self.controller.mostrar_frame(Principal)

    def abrir_menu_cadastro(self):
        self.controller.mostrar_frame()