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
        x.execute("select * from paciente ")
        result = x.fetchall()
        Label(porta,text="Nome").grid(row=1,column=1,pady=5)
        Label(porta, text="CPF").grid(row=1, column=2,pady=5)
        Label(porta, text="Telefone").grid(row=1, column=3,pady=5)
        for i,row in enumerate(result):
                Label(porta,text= f"{row[1]}").grid(row= i+5 ,column=1,pady=5,padx=5)
                Label(porta, text=f"{row[0]}").grid(row= i +5 ,column=2,pady=5,padx=5)
                Label(porta, text=f"{row[2]}").grid(row=i + 5, column=3, pady=5, padx=5)





avaliar()
porta.mainloop()