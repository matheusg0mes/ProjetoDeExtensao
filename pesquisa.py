import mysql.connector
from tkinter import *
import tkinter.messagebox as MessageBox

conecao = mysql.connector.connect( host ="localhost", user="root", passwd="", database ="bd")

x = conecao.cursor()

#x.execute('create database  bd')

x.execute("use bd")

#x.execute(''' create table paciente(cpf varchar(11) primary key,
#          nome varchar(100),
 #         celular varchar(20),
 #         frequencia varchar(100),
 #         restricao varchar(100),
 #         responsalvel varchar(100),
 #         escolaridade varchar(100),
  #        funcionario varchar(100))'''
#        )
v =[("111-111-111-11","matheus","11111-1111","2 dias","leite","robson","2 ano","julia"),
    ("222-222-222-22","roger","11111-1111","3 dias","pao","robson","4 ano","kid"),
    ("333-333-333-33","matheus","11111-1111","4 dias","leite","robson","1 ano","bengala")]
#x.executemany("insert into paciente(cpf,nome,celular,frequencia,restricao,responsalvel,escolaridade,funcionario) values(%s,%s,%s,%s,%s,%s,%s,%s)",v)
#conecao.commit()
#print(x.rowcount)
#p = ["matheus"]
#x.execute('select * from paciente where nome=%s ', p)
#r = x.fetchall()
#for i in r:
#    print(i)

porta = Tk()
porta.geometry("500x500")
def avaliar():
    cpf = e_pesquisa.get()
    if cpf == "":
        MessageBox.showinfo("Error","O campo não pode ser vazio")
    else:
        x.execute("select * from paciente where cpf=%s",(cpf,))
        result = x.fetchall()
        op = Tk()
        op.geometry('500x500')
        for row in result:
            Label(op,text= f"Cpf: {row[0]}").place(x=10,y=10)
            Label(op, text=f"Nome: {row[1]}").place(x=10, y=30)
            Label(op, text=f"Celular: {row[2]}").place(x=10, y=50)
            Label(op, text=f"Frequencia: {row[3]}").place(x=10, y=70)
            Label(op, text=f"Restrição: {row[4]}").place(x=10, y=90)
            Label(op, text=f"Responsavel: {row[5]}").place(x=10, y=110)
            Label(op, text=f"Escolaridade: {row[6]}").place(x=10, y=130)
            Label(op, text=f"Funcionario: {row[7]}").place(x=10, y=150)




Label(porta,text="Pesquisar:").place(x=10,y=20)

e_pesquisa = Entry(porta)
e_pesquisa.place(x=100,y=20)

resultado_label = Label(porta,bg="#CECECE")
Button(porta,text="Consultar",command=avaliar).place(x=50,y=50)
porta.mainloop()