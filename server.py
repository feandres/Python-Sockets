import socket
import threading
import time

conexoes = []
mensagens = []
login_list = []
adminconn = ""
flag_close = False
flag = True


def start():
    global flag
    global conexoes
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER = socket.gethostbyname(socket.gethostname())
    PORT = 8080
    ADDR = (SERVER, PORT)
    print(f"[INICIANDO SOCKET: {SERVER}:{PORT}]")
#Le arquivos de logins e senhas
    with open("login.txt","r") as login:
        for line in login:
            login_list.append(line.strip())
    try:
#Começa a esperar por conexões
        server.bind(ADDR)
        server.listen()
    except:
        return print('\nNão foi possível iniciar o servidor!\n')
#Loop para iniciar threads para cada client novo 
    while(flag):
        conn, addr = server.accept()
        thread = threading.Thread(target = clientThread, args=(conn, addr))
        thread.start()

    server.close()

#Envia historico de mensagens para client e atualiza seu historico de leitura visando igualar
#o marcador last para o total de mensagens enviadas
def individualMsg(conexao):
    print(f"[ENVIANDO] Enviando mensagens para {conexao['addr']}")
    for i in range(conexao['last'], len(mensagens)):
        mensagem_de_envio = "msg=" + mensagens[i]
        conexao['conn'].send(mensagem_de_envio.encode('utf-8'))
        conexao['last'] = i + 1
        time.sleep(0.2)
#Enviar mensagem para todos os clients exceto o que enviou
def sendAllMsg(conn):
    global conexoes
    for conexao in conexoes:
        if(conexao["conn"] != conn):
            individualMsg(conexao)

def clientThread(conn, addr):
    print(f"[NOVA CONEXAO] Um novo usuario se conectou pelo endereço {addr}")
    global conexoes 
    global mensagens
    global adminconn
    global flag
    msg_dc = "!quit"

    flag_client = True
    flag_login = False

    usern = conn.recv(2048).decode('utf-8')
    passw = conn.recv(2048).decode('utf-8')

    count = 0
#Autenticar login
    for i in login_list:
        login_split = i.split(":")
        if login_split[0]==usern and login_split[1]==passw:
            flag_login = True
            break
        count += 1
#Certificar que o usuario ja nao esta logado
    for i in conexoes:
        if i["username"] == usern:
            flag_login = False
            break

#Caso a autenticação funcione, segue
    if flag_login:
        succesmsg = "success"
        conn.send(succesmsg.encode())
        #armazena informações dos clients
        mapa_da_conexao = {
           "conn": conn,
           "addr": addr,
           "username": usern,
           "last": 0,
           "logado": True
        }
        if(usern == "admin"):
            adminconn = conn

        print(f"[CONFIRMAÇÃO LOGIN] {usern} se conectou pelo endereço {addr}")
        conexoes.append(mapa_da_conexao)
        individualMsg(mapa_da_conexao)
#loop para tratar mensagens
        while flag_client:
            msg = conn.recv(2048).decode('utf-8')
            if msg.startswith("msg="):
                mensagem_separada = msg.split("=")
                mensagem = usern + "=" + mensagem_separada[1]
                #sessao para comando shutdown
                if(conn == adminconn):
                    if(mensagem_separada[1] == "!shutdown"):
                        contador = 10
                        #countdown de 10s
                        for i in range(10):
                            msg_shutdown = "msg=" + usern + "=O servidor irá encerrar em " + str(contador) + "s"
                            contador -= 1
                            conn.send(msg_shutdown.encode('utf-8'))
                            time.sleep(1)
                        #desconecta todos
                        for conexao in conexoes:
                            conexao["conn"].send(msg_dc.encode('utf-8'))
                        flag_client = False
                        flag = False
                        break
                #desconecta individualmente quem requisitar sair
                if(mensagem_separada[1] == "!quit"):
                    removeClient(conn)
                    flag_client = False
                    mensagem = "ADMIN=O usuário " + usern + " saiu da conversa"
                #simplesmente agrega mensagem ao log de mensagens e envia para todos depois
                mensagens.append(mensagem)
                sendAllMsg(conn)
            else:
                removeClient(conn)
            if not msg:
                break
    else:
        succesmsg = "failure"
        conn.send(succesmsg.encode())
#remover client individualmente
def removeClient(conn):
    global conexoes
    for conexao in conexoes:
        if(conexao["conn"] == conn):
            conn.close()
            conexoes.remove(conexao)

start()


