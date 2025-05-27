import customtkinter as tk
from tkinter import messagebox
import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gerenciamento"
)
x = conexao.cursor()

tk.set_appearance_mode("light")
tema = ["light"]

def temanovo():
    novotema = "dark" if tema[0] == "light" else "light"
    tk.set_appearance_mode(novotema)
    tema[0] = novotema
    if novotema == "dark":
        btntema.configure(text="\U0001F319")
    else:
        btntema.configure(text="\u2600")


def validar_cpf(cpf):
    if len(cpf) != 14 or cpf[3] != '.' or cpf[7] != '.' or cpf[11] != '-':
        messagebox.showerror("CPF inválido", "O CPF deve ser digitado no modelo 000.000.000-00.")
        return False
    cpf_numeros = ''.join(c for c in cpf if c.isdigit())
    if len(cpf_numeros) != 11 or cpf_numeros == cpf_numeros[0] * 11:
        messagebox.showerror("CPF inválido", "Digite o CPF novamente!")
        return False
    soma1 = sum(int(cpf_numeros[i]) * (10 - i) for i in range(9))
    digito1 = (soma1 * 10 % 11) % 10
    soma2 = sum(int(cpf_numeros[i]) * (11 - i) for i in range(10))
    digito2 = (soma2 * 10 % 11) % 10
    if digito1 != int(cpf_numeros[9]) or digito2 != int(cpf_numeros[10]):
        messagebox.showerror("CPF inválido", "Digite o CPF novamente!")
        return False
    return True

def sair_tela_cheia(event=None):
    porta.attributes('-fullscreen', False)

porta = tk.CTk()
porta.wm_iconbitmap('favicon.ico')
porta.geometry(f"{porta.winfo_screenwidth()}x{porta.winfo_screenheight()}+0+0")
porta.bind("<Escape>", sair_tela_cheia)
porta.title("Buscar Paciente")

titulo_principal = tk.CTkLabel(porta,text="Buscar Pacientes",font=("Arial", 28, "bold"))
titulo_principal.pack(pady=(170, 50))

frame_central = tk.CTkFrame(porta)
frame_central.place(relx=0.5, rely=0.5, anchor='center')

tk.CTkLabel(frame_central, text="CPF", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
e_pesquisa = tk.CTkEntry(frame_central, width=250, font=("Arial", 14))
e_pesquisa.grid(row=0, column=1, padx=10, pady=10)

btn_buscar = tk.CTkButton(frame_central, text="Buscar", command=lambda: buscar())
btn_buscar.grid(row=1, column=0, columnspan=2, pady=(0,20))

resultado_frame = tk.CTkFrame(frame_central)
resultado_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

btntema = tk.CTkButton(frame_central, text="\u2600", command=temanovo)
btntema.grid(row=3, column=0, columnspan=2, pady=20)

def buscar():
    cpf = e_pesquisa.get()
    if not validar_cpf(cpf):
        return

    x.execute("SELECT * FROM pessoas WHERE cpf = %s", (cpf,))
    result = x.fetchall()

    for widget in resultado_frame.winfo_children():
        widget.destroy()

    if not result:
        messagebox.showinfo("Erro", "Paciente não encontrado")
        return

    campos = ["ID", "Nome", "CPF", "Celular", "Responsável", "Endereço","Frequência", "Escolaridade", "Atendido", "Restrição","Acompanhado por", "Sexo"]

    for i, valor in enumerate(result[0]):
        tk.CTkLabel(resultado_frame, text=f"{campos[i]}:", anchor="e", width=20, font=("Arial", 12, "bold")).grid(row=i, column=0, padx=5, pady=3, sticky="e")
        tk.CTkLabel(resultado_frame, text=str(valor), anchor="w", width=50, font=("Arial", 12)).grid(row=i, column=1, padx=5, pady=3, sticky="w")

porta.mainloop()
