import mysql.connector
from tkinter import messagebox

def conectar_mysql():
    conn = mysql.connector.connect(
        host='maglev.proxy.rlwy.net',
        port=42726,
        user='root',
        password='IYFvHMUzhUAhURDvhvcwrLPZcUGIwVPK',
        database='railway'
    )
    return conn, conn.cursor()


def validarcpf(cpf):
    if len(cpf) != 14 or cpf[3] != '.' or cpf[7] != '.' or cpf[11] != '-':
        messagebox.showerror("CPF inválido", "O CPF deve ser digitado no modelo 000.000.000-00.")
        return False
    numeros = ''.join(c for c in cpf if c.isdigit())
    if len(numeros) != 11 or numeros == numeros[0] * 11:
        messagebox.showerror("CPF inválido", "Digite o CPF novamente!")
        return False
    soma1 = sum(int(numeros[i]) * (10 - i) for i in range(9))
    digito1 = (soma1 * 10 % 11) % 10
    soma2 = sum(int(numeros[i]) * (11 - i) for i in range(10))
    digito2 = (soma2 * 10 % 11) % 10
    if digito1 != int(numeros[9]) or digito2 != int(numeros[10]):
        messagebox.showerror("CPF inválido", "Digite o CPF novamente!")
        return False
    return True
