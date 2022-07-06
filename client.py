import socket
import threading
import os

#                             IPv4            TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
flag = True
#Enviar mensagem para server
#Se for comando para sair, altera flag para false para encerrar o client
def sendMsg():
    global flag
    try:
        mensagem = input()
        if(mensagem == "!quit"):
            flag = False
        mensagem = "msg=" + mensagem
        client.send(mensagem.encode('utf-8'))
    except:
        return
#Enviar username seguido de senha
def setlogin():
    username = input('Username: ')
    password = input('Password: ')
    client.send(username.encode('utf-8'))
    client.send(password.encode('utf-8'))


def start():
    global flag
    #Usuario insere endereço IP seguido da Porta
    SERVER = input("Insira o HOSTNAME(EndereçoIPv4:Porta): ") #IPv4
    addres_port = SERVER.split(":")
    ADDR = (addres_port[0], int(addres_port[1]))

    try:
        #Conecta ao server
        client.connect(ADDR)
        setlogin()
        msg = client.recv(2048).decode()
        if(msg != "success"):
            print("\nLogin inválido")
            client.close()
        else:
            os.system("cls")
            print("[CONECTADO]")
            threading.Thread(target=handleMsg).start()
            while(flag):
                sendMsg()
            client.close()
            os.system("exit")
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')
    
#Thread para receber mensagens e repassar ao usuário
def handleMsg():
    global flag
    while(flag):
        try:
            msg = client.recv(2048).decode()
            mensagem_splitada = msg.split("=")
            if(msg == "!quit"):
                flag = False
                mensagem = "msg=!quit"
                client.send(mensagem.encode('utf-8'))
            print(mensagem_splitada[1] + ": " + mensagem_splitada[2])
        except:
            break

start()


