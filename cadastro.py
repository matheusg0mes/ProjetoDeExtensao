import tkinter as tk
from tkinter import messagebox
import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gerenciamento"
)
x = conexao.cursor()
#x.execute('create database gerenciamento')
#x.execute('use gerenciamento')

x.execute("""
CREATE TABLE IF NOT EXISTS pessoas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cpf VARCHAR(14),
    celular VARCHAR(15),
    responsavel VARCHAR(50),
    endereco VARCHAR(100),
    frequencia VARCHAR(20),
    escolaridade VARCHAR(50),
    atendido VARCHAR(10),
    restricao VARCHAR(50),
    encarregado VARCHAR(50),
    sexo VARCHAR(10)
)
""")
conexao.commit()

def validarcpf(cpf):
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

def cadastrar():
    nome = entry_nome.get()
    cpf = entry_cpf.get()
    celular = entry_celular.get()
    responsavel = entry_responsavel.get()
    endereco = entry_endereco.get()
    frequencia = entry_frequencia.get()
    escolaridade = entry_escolaridade.get()
    restricao = entry_restricao.get()
    encarregado = entry_encarregado.get()
    sexo = entry_sexo.get()
    atendido = "Sim" if var_atendido.get() == 1 else "Não"

    if not all([nome, cpf, celular, responsavel, endereco, frequencia, escolaridade, restricao, encarregado, sexo]):
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
        return

    if not validarcpf(cpf):
        return

    x.execute("""
        INSERT INTO pessoas (
            nome, cpf, celular, responsavel, endereco, frequencia, escolaridade, atendido, restricao, encarregado, sexo
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (nome, cpf, celular, responsavel, endereco, frequencia, escolaridade, atendido, restricao, encarregado, sexo))
    conexao.commit()

    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
    entry_nome.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_celular.delete(0, tk.END)
    entry_responsavel.delete(0, tk.END)
    entry_endereco.delete(0, tk.END)
    entry_frequencia.delete(0, tk.END)
    entry_escolaridade.delete(0, tk.END)
    entry_restricao.delete(0, tk.END)
    entry_encarregado.delete(0, tk.END)
    entry_sexo.delete(0, tk.END)
    var_atendido.set(0)

root = tk.Tk()
root.title("Cadastro de Pessoa")
root.geometry("800x350")

labels = [
    "Nome", "CPF",
    "Celular", "Responsável",
    "Endereço", "Frequência",
    "Escolaridade", "Restrição",
    "Acompanhado por", "Sexo"
]
entradas = []

for i, label_text in enumerate(labels):
    row = i // 2
    col = (i % 2) * 2
    tk.Label(root, text=label_text + ":").grid(row=row, column=col, sticky="e", padx=10, pady=10)
    entry = tk.Entry(root, width=30)
    entry.grid(row=row, column=col + 1, sticky="w", padx=10, pady=10)
    entradas.append(entry)

entry_nome, entry_cpf, entry_celular, entry_responsavel, entry_endereco, entry_frequencia, entry_escolaridade, entry_restricao, entry_encarregado, entry_sexo = entradas

var_atendido = tk.IntVar()
tk.Label(root, text="Atendido:").grid(row=5, column=0, sticky="e", padx=10, pady=10)
check = tk.Checkbutton(root, text="Sim", variable=var_atendido)
check.grid(row=5, column=1, sticky="w", padx=10, pady=10)

btncadastrar = tk.Button(root, text="Cadastrar", command=cadastrar, width=20, bg="green", fg="white")
btncadastrar.grid(row=6, column=0, columnspan=4, pady=30)

root.mainloop()
