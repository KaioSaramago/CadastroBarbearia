#!/usr/bin/python
# -*- coding: UTF-8 -*-
from Tkinter import *
from datetime import date
import sqlite3
import tkMessageBox
import ttk
import os
import time

#variaveis
janela = Tk()
logado = "nenhum"
socio = "nenhum"

con1 = sqlite3.connect('serv.db')
c1 = con1.cursor()
con2 = sqlite3.connect('barbeiros.db')
c2 = con2.cursor()
con3 = sqlite3.connect('socios.db')
c3 = con3.cursor()
                             
c1.execute('CREATE TABLE IF NOT EXISTS serv(barbeiro text, servico text,preco int,data text )')
c2.execute('CREATE TABLE IF NOT EXISTS barbeiros(nome text, login text,senha text,porcentagem text)')
c3.execute('CREATE TABLE IF NOT EXISTS socios(nome text, login text,senha text)')

"""################### DESCOMENTE AS PROXIMAS linhas para criar o cadastro DEFAULT #################################################################################"""
#c3.execute("INSERT INTO socios VALUES ('Admin','admin','123')")
#con3.commit()

#FUNÇÃO RESPONSÁVEL PELO CADASTRO DE BARBEIROS.
def cadastrarbarbeiro():
    global socio
    if(socio == "sim"):
        def InserirNObarbeiros():
            c2.execute("INSERT INTO barbeiros VALUES(?,?,?,?)",(nome_barbeiro.get(),login_barbeiro.get(),senha_barbeiro.get(),porcentagem.get()))
            con2.commit()
            time.sleep(1)
            tkMessageBox.showinfo("Cadastro feito com sucesso!","As informações do barbeiro foram salvas no banco de dados.")
            nome_barbeiro.delete(0,END)
            login_barbeiro.delete(0,END)
            senha_barbeiro.delete(0,END)
            porcentagem.delete(0,END)
        def testebarbeiro():#testa se barbeiro ja existe
            c2.execute('SELECT * FROM barbeiros WHERE login="%s" AND senha="%s" ' % (login_barbeiro.get(), senha_barbeiro.get()))
            if c2.fetchone() is not None:
                tkMessageBox.showinfo("Cadastro não realizado!","Já existe um barbeiro com o login: %s "% login_barbeiro.get())
            else:
                if(porcentagem.get().isdigit()==True):
                    InserirNObarbeiros()
                else:
                    if(len(nome_barbeiro.get())>=4 and len(senha_barbeiro.get())>=4 and len(login_barbeiro.get())>=4):
                        tkMessageBox.showinfo("Cadastro não realizado!","Porcentagem não é um inteiro")
                        porcentagem.delete(0, END)
                    else:
                        tkMessageBox.showinfo("Cadastro não realizado!", "Nome ou Login ou Senha devem ter no mínimo 4 caracteres")

        janelaCadastroBarbeiro = Tk()
        Label(janelaCadastroBarbeiro, text= "Nome do barbeiro:").grid(row=1,column=3)
        nome_barbeiro = Entry(janelaCadastroBarbeiro, width = 25)
        nome_barbeiro.grid(row=2,column=3)
        Label(janelaCadastroBarbeiro, text= "Login:").grid(row=4,column=3)
        login_barbeiro = Entry(janelaCadastroBarbeiro, width = 25)
        login_barbeiro.grid(row=5,column=3)
        Label(janelaCadastroBarbeiro, text= "Senha:").grid(row=6,column=3)
        senha_barbeiro = Entry(janelaCadastroBarbeiro, width = 25)
        senha_barbeiro.grid(row=7,column=3)
        Label(janelaCadastroBarbeiro, text= "Porcentagem de lucro:").grid(row=8, column=3)
        porcentagem = Entry(janelaCadastroBarbeiro, width=25)
        porcentagem.grid(row=9, column=3)
        Button(janelaCadastroBarbeiro, width = 25,text = "Cadastrar",command = testebarbeiro).grid(row = 10, column = 3)
        janelaCadastroBarbeiro.geometry("300x300+0+0")
        janelaCadastroBarbeiro.title("Cadastrar Barbeiro")
        janelaCadastroBarbeiro.mainloop()
    else:
        tkMessageBox.showinfo("Cadastro não realizado!","É necessário estar logado como sócio para ter acesso à essa opcão.")

#FUNÇÃO RESPONSÁVEL PELO CADASTRO DE SÓCIOS.
def cadastrarsocio():
    global socio
    if (socio == "sim"):

        def InserirNOsocios():
            c3.execute("INSERT INTO socios VALUES(?,?,?)",(nome_socio.get(),login_socio.get(),senha_socio.get()))
            con3.commit()
            time.sleep(1)
            tkMessageBox.showinfo("Cadastro feito com sucesso!","As informações do sócio foram salvas no banco de dados.")
            nome_socio.delete(0,END)
            login_socio.delete(0,END)
            senha_socio.delete(0,END)

        def testesocio():
            c3.execute('SELECT * FROM socios WHERE login="%s" AND senha="%s" ' % (login_socio.get(), senha_socio.get()))
            if c3.fetchone() is not None:
                tkMessageBox.showinfo("Cadastro não realizado!","Já existe um barbeiro com o login: %s " % login_socio.get())
            else:
                if (len(nome_socio.get()) >= 4 and len(senha_socio.get()) >= 4 and len(login_socio.get()) >= 4):
                    InserirNOsocios()
                else:
                    tkMessageBox.showinfo("Cadastro não realizado!","Nome ou Login ou Senha devem ter no mínimo 4 caracteres")

        janelaCadastroSocio = Tk()
        Label(janelaCadastroSocio, text= "Nome do sócio:").grid(row=1,column=3)
        nome_socio = Entry(janelaCadastroSocio, width = 25)
        nome_socio.grid(row=2,column=3)
        Label(janelaCadastroSocio, text= "Login:").grid(row=4,column=3)
        login_socio = Entry(janelaCadastroSocio, width = 25)
        login_socio.grid(row=5,column=3)
        Label(janelaCadastroSocio, text= "Senha:").grid(row=7,column=3)
        senha_socio = Entry(janelaCadastroSocio, width = 25)
        senha_socio.grid(row=8,column=3)
        botao = Button(janelaCadastroSocio, width = 25,text = "Cadastrar",command = testesocio).grid(row = 9, column = 3)
        janelaCadastroSocio.geometry("300x300+0+0")
        janelaCadastroSocio.title("Cadastrar Sócio")
        janelaCadastroSocio.mainloop()
    else:
        tkMessageBox.showinfo("Cadastro não realizado!", "É necessário estar logado como sócio para ter acesso à essa opção.")

#FUNÇÃO RESPONSÁVEL POR GERAR O RELATÓRIO EM TXT.    
def gerar_relatorio():
    global socio
    if (socio == "sim"):
        hj = date.today()
        arq = open('Relatorio.txt', 'w')
        arq.write('Relatorio \n\n')
        for k in range(0,31):
            c1.execute('SELECT barbeiro,servico,preco FROM serv WHERE data="%s"'%(date.fromordinal(hj.toordinal() - k)))
            arq.write(str("%s\n"%(date.fromordinal(hj.toordinal() - k))))
            rows = c1.fetchall()
            for linha in rows:
                arq.write(str(linha))
                arq.write("\n")
            arq.write("\n\n")
        arq.close()
        os.system('Relatorio.txt')
    else:
        tkMessageBox.showinfo("Sem permissão!","É necessário estar logado como sócio para ter acesso à essa opção.")

#FUNÇÃO RESPONSÁVEL POR VERIFICAR A SITUAÇÃO DE UM BARBEIRO(GANHOS COM BASE NA PORCENTAGEM DE CADA BARBEIRO).    
def situacao_barbeiro():
    somadia = 0
    somadian = 0.0
    global socio
    global en2
    por = 0
    if (socio == "sim"):
        hj = date.today()
        arq = open('situacao.txt', 'w')
        arq.write('situacao \n\n')
        for k in range(0, 31):
            somadia = 0
            c1.execute('SELECT * FROM serv WHERE data="%s" and barbeiro ="%s"' % (date.fromordinal(hj.toordinal() - k),en2.get()))
            arq.write(str("%s\n" % (date.fromordinal(hj.toordinal() - k))))
            rows = c1.fetchall()
            for linha in rows:
                arq.write(str(linha))
                arq.write("\n")
            arq.write("\n\n")
            c1.execute('SELECT preco FROM serv WHERE data="%s" and barbeiro ="%s"' % (date.fromordinal(hj.toordinal() - k), en2.get()))
            for row in c1.fetchall():
                somadia = somadia + row[0]
            arq.write("Ganho total durante o dia: %s " %somadia)

            c2.execute('SELECT * FROM barbeiros WHERE login="%s"' % en2.get())
            if c2.fetchone() is not None:
                print "Barbeiro"
                c2.execute('SELECT porcentagem FROM barbeiros WHERE login="%s"' % en2.get())
                for k in c2.fetchall():
                    por=k[0]

                somadian = somadia*float(por)/100
            else:
                c3.execute('SELECT * FROM socios WHERE login="%s"' % en2.get())
                if c3.fetchone() is not None:
                    print "Sócio"
                    somadian = somadia
            arq.write("\nGanho descontado durante o dia: %s\n\n" % somadian)
        arq.close()
        os.system('situacao.txt')
    else:
        tkMessageBox.showinfo("Sem permissão!", "É necessário estar logado como sócio para ter acesso à essa opção.")

#FUNÇÃO RESPONSÁVEL PELO LOGOUT.        
def logout():
    global logado
    global socio
    janela.title("Página inicial")
    logado = "nenhum"
    socio = "nenhum"
    Label(janela, width=25, text="Logout Realizado",bg="white").grid(row=6, column=1)

#FUNÇÃO RESPONSÁVEL POR VERIFICAR OS DADOS DIGITADOS PELO USUÁRIO NO BANCO DE DADOS PARA PERMITIR O ACESSO ÀS OPÇÕES DO SOFTWARE.
def validardados():
    global logado
    global socio
    c2.execute('SELECT * FROM barbeiros WHERE login="%s" AND senha="%s" '%(login.get(),senha.get()))
    if c2.fetchone() is not None:
        print c2.fetchone()
        k = Label(janela,width = 25, text="Usuário Encontrado",bg="white")
        k.grid(row=6, column=1)
        tkMessageBox.showinfo("Barbeiro(a) encontrado", "As opções de barbeiro(a) estão liberadas.")
        logado=login.get()
        socio = "nao"
        janela.title("%s - Barbeiro(a)" % login.get())
        login.delete(0, END)
        senha.delete(0, END)
    else:
        c3.execute('SELECT * FROM socios WHERE login="%s" AND senha="%s" '%(login.get(),senha.get()))
        if c3.fetchone() is not None:
            k = Label(janela,width = 25, text="Usuário Encontrado",bg="white")
            k.grid(row=6, column=1)
            tkMessageBox.showinfo("Sócio encontrado", "As opções de sócios estão liberadas.")
            logado = login.get()
            socio = "sim"
            janela.title("%s - Sócio(a)" %login.get())
            login.delete(0, END)
            senha.delete(0, END)
        else:
            k = Label(janela,width = 25, text="Usuário não cadastrado",fg="red",bg="white")
            k.grid(row=6,column=1)
            tkMessageBox.showinfo("Usuário não encontrado!","É necessário logar-se para ter acesso às opções.")
            login.delete(0, END)
            senha.delete(0, END)
            socio = "nenhum"
            logado = "nenhum"

#FUNÇÃO RESPONSÁVEL POR CALCULAR O PREÇO TOTAL COM BASE NAS OPÇÕES ESCOLHIDAS PELO USUÁRIO.
def calcularpreco():
    x=0
    if (var1.get()==1):
        x=10 #preco do corte normal
    if (var2.get() == 1):
        x = x + 15 #preco do corte especial
    if (var3.get() == 1):
        x = x + 10  # preco da barba
    if (var4.get() == 1):
        x = x + 15  # preco da barba especial
    return x

#FUNÇÃO RESPONSÁVEL POR EXIBIR O PREÇO TOTAL.
def mostrarpreco():
    en1.delete(0,END)
    en1.insert(0, "%s" % calcularpreco())

#FUNÇÃO RESPONSÁVEL POR SALVAR INFORMAÇÕES NO BANCO DE DADOS.   
def salvarnobanco():
    if (logado == "nenhum"):
        tkMessageBox.showinfo("Login não detectado!", "Para salvar informações no banco de dados é necessário estar logado.")
    else:
        c1.execute("INSERT INTO serv VALUES ('%s','%s','%d','%s')" % (logado, servicos(), calcularpreco(),date.today()))
        print servicos()
        print calcularpreco()
        print logado
        con1.commit()
        tkMessageBox.showinfo("Sucesso!", "Informações salvas no banco de dados\n\nPrestador de serviço: %s\nServiço(s)prestados: %s\nPreço: %d"% (logado, servicos(), calcularpreco()))

#FUNÇÃO RESPONSÁVEL POR RETORNAR AS STRINGS COM AS OPÇÕES ESCOLHIDAS PELO USUÁRIO.
def servicos():
    x = " "
    if (var1.get() == 1):
            x = "Corte"
    if (var2.get() == 1):
            x = x + ", Corte especial"
    if (var3.get() == 1):
            x = x + ", Barba"
    if (var4.get() == 1):
            x = x + ", Barba especial"
    return x

#FUNÇÃO RESPONSÁVEL POR REMOVER SÓCIO.
def remover_socio():
    global socio
    global logado
    global c3
    if (socio == "sim" ):
        def deletar_socio():
            global c3
            if logado == str(login.get()):
                c3.execute('SELECT * FROM socios WHERE login = "%s" '% login.get())
                if c3.fetchall() is not None:
                    if (tkMessageBox.askyesno("Confirmação de exclusão","Tem certeza que deseja excluir?")) == True:
                        c3.execute('DELETE FROM socios WHERE login = "%s" ' % login.get())
                        con3.commit()
                        nome_socio.delete(0, END)
                        login.delete(0, END)
                        logout()
                else:
                    tkMessageBox.showinfo("Nenhum sócio encontrado!","Tente digitar o login novamente.")
            else:
                tkMessageBox.showinfo("Erro", "Apenas o próprio sócio pode se excluir.")
        janeladeletarsocio = Tk()
        Button(janeladeletarsocio, width=25, text="Gerar relação de sócios", command=gerar_socios).grid(row=1, column=1)
        Label(janeladeletarsocio, text="Nome do sócio:").grid(row=2, column=1)
        nome_socio = Entry(janeladeletarsocio, width=25)
        nome_socio.grid(row=3, column=1)
        Label(janeladeletarsocio, text="Login:").grid(row=4, column=1)
        login=Entry(janeladeletarsocio, width=25)
        login.grid(row=5, column=1)
        Button(janeladeletarsocio, width=25, text="DELETAR", command=deletar_socio).grid(row=10, column=1)
        janeladeletarsocio.geometry("300x300+0+100")
        janeladeletarsocio.title("DELETAR SÓCIO")
        janeladeletarsocio.mainloop()
    else:
        tkMessageBox.showinfo("Erro!","É necessário estar logado como sócio para ter acesso à essa opção.")

#FUNÇÃO RESPONSÁVEL POR GERAR SÓCIOS EM ARQUIVO TXT.       
def gerar_socios():
    arq = open('socios.txt', 'w')
    arq.write('Sócios \n\nNomes/Logins\n\n ')
    c3.execute('SELECT nome,login FROM socios')
    rows = c3.fetchall()
    for row in rows:
        arq.write(str(row))
        arq.write("\n")
        print row
    arq.close()
    os.system('socios.txt')

#FUNÇÃO RESPONSÁVEL POR GERAR BARBEIROS EM ARQUIVO TXT.    
def gerar_barbeiros():
    arq = open('barbeiros.txt', 'w')
    arq.write('Barbeiros \n\nNomes/Logins\n\n ')
    c2.execute('SELECT nome,login FROM barbeiros')
    rows = c2.fetchall()
    for row in rows:
        arq.write(str(row))
        arq.write("\n")
        print row
    arq.close()
    os.system('barbeiros.txt')

#FUNÇÃO RESPONSÁVEL POR REMOVER BARBEIRO.    
def remover_barbeiro():
    global socio
    global c2
    if (socio == "sim"):
        def deletar_barbeiro():
            global c2
            c2.execute('SELECT * FROM barbeiros WHERE login = "%s" ' % login.get())
            if c2.fetchall() is not None:
                if (tkMessageBox.askyesno("Confirmação de exclusão", "Tem certeza que deseja excluir?")) == True:
                    c2.execute('DELETE FROM barbeiros WHERE login = "%s" ' % login.get())
                    con2.commit()
                    nome_barbeiro.delete(0, END)
                    login.delete(0, END)
                    Label(janela, width=25, text="Barbeiro Removido", bg="white").grid(row=6, column=1)
            else:
                tkMessageBox.showinfo("Nenhum barbeiro encontrado!", "Tente digitar o login novamente.")
        janeladeletarbarbeiro = Tk()
        Button(janeladeletarbarbeiro, width=25, text="Gerar relação de barbeiros", command=gerar_barbeiros).grid(row=1, column=1)
        Label(janeladeletarbarbeiro, text="Nome do Barbeiro:").grid(row=2, column=1)
        nome_barbeiro = Entry(janeladeletarbarbeiro, width=25)
        nome_barbeiro.grid(row=3, column=1)
        Label(janeladeletarbarbeiro, text="Login:").grid(row=4, column=1)
        login = Entry(janeladeletarbarbeiro, width=25)
        login.grid(row=5, column=1)
        Button(janeladeletarbarbeiro, width=25, text="DELETAR", command=deletar_barbeiro).grid(row=10, column=1)
        janeladeletarbarbeiro.geometry("300x300+0+100")
        janeladeletarbarbeiro.title("DELETAR BARBEIRO")
        janeladeletarbarbeiro.mainloop()
    else:
        tkMessageBox.showinfo("Cadastro não realizado",
                              "É necessário estar logado como sócio para ter acesso à essa opção.")


#variáveis do registro de pedido
var1 = IntVar()
Checkbutton(janela, text="Corte", variable=var1).grid(row=5, column=3,sticky=W)
var2 = IntVar()
Checkbutton(janela, text="Corte especial", variable=var2).grid(row=6, column=3,sticky=W)
var3 = IntVar()
Checkbutton(janela, text="Barba", variable=var3).grid(row=7, column=3,sticky=W)
var4 = IntVar()
Checkbutton(janela, text="Barba especial", variable=var4).grid(row=8, column=3,sticky=W)

#Entry
en1 = Entry(janela, width=25)
en1.grid(row=4,column=4)
en2 = Entry(janela, width=25)
en2.grid(row=8,column=7)
login = Entry(janela, width = 25)
login.grid(row=2,column=1)
senha = Entry(janela, width = 25,show='*')
senha.grid(row=4,column=1)

#botões
bt9 = Button(janela, width=25, text="Salvar no banco de dados",command=salvarnobanco, fg = "blue", bg = "gray", relief ="ridge", font ="Calibri").grid(row=12, column=3)
Button(janela, width = 25,text = "Cadastrar Barbeiro",command=cadastrarbarbeiro, fg = "blue", bg = "gray", relief ="ridge", font ="Calibri").grid(row = 4, column = 6)
Button(janela, width = 25,text = "Barbeiros cadastrados",command=gerar_barbeiros, fg = "blue", bg = "gray", relief ="ridge", font ="Calibri").grid(row = 4, column = 7)
Button(janela, width = 25,text = "Cadastrar Sócio",command=cadastrarsocio, fg = "blue", bg = "gray", relief ="ridge", font ="Calibri").grid(row = 5, column = 6)
Button(janela, width = 25,text = "Sócios cadastrados",command=gerar_socios, fg = "blue", bg = "gray", relief ="ridge", font ="Calibri").grid(row = 5, column = 7)
Button(janela, width = 25,text = "Remover Barbeiro",command = remover_barbeiro, fg = "red", bg = "gray", relief ="ridge", font ="Calibri").grid(row = 6, column = 6)
Button(janela, width = 25,text = "Remover Sócio",command = remover_socio, fg = "red", bg = "gray", relief ="ridge", font ="Calibri").grid(row = 7, column = 6)
Button(janela, width = 25,text = "Gerar relatório em txt",command = gerar_relatorio, fg = "blue", bg = "gray", relief ="ridge", font ="Calibri").grid(row = 8, column = 6)
Button(janela, width = 25,text = "Calcular preço",command =mostrarpreco, fg = "blue", bg = "gray", relief ="ridge", font ="Calibri").grid(row = 9, column = 3)
Button(janela, width = 25,text = "Validar dados",command =validardados, fg = "blue", bg = "gray", relief ="ridge", font ="Calibri").grid(row = 5, column = 1)
Button(janela, width = 25,text = "Pesquisar",command =situacao_barbeiro, fg = "blue", bg = "gray", relief ="ridge", font ="Calibri").grid(row = 9, column = 7)
Button(janela, width = 25,text = "Logout",command =logout, fg = "blue", bg = "gray", relief ="ridge", font ="Calibri").grid(row = 7, column = 1)

#labels
ttk.Separator(janela,orient=HORIZONTAL).grid(row=1, columnspan=5,column = 5,sticky="ew")
ttk.Separator(janela,orient=HORIZONTAL).grid(row=1, columnspan=5,column = 2,sticky="ew")
Label(janela, text= "Login", relief="ridge").grid(row=1,column=1)
Label(janela, text= "Pesquisar situação de barbeiro:", relief="ridge").grid(row=7,column=7)
Label(janela, text= "Senha", relief="ridge").grid(row=3,column=1)
Label(janela, text= "Menu Barbeiro:", relief="ridge").grid(row=1,column=3)
Label(janela, text= "Menu Sócio:", relief="ridge").grid(row=1,column=6)
Label(janela, text= "Registrar serviço:", relief="ridge").grid(row=3,column=3)
Label(janela, text= "Preço:", relief="ridge").grid(row=3,column=4)

#definições da janela principal
janela.geometry("1000x500+200+150")
janela.resizable(width=False,height=False)
janela.title("Página inicial")
janela.mainloop()

#con1.close()
#con2.close()