import socket 
import threading
import time
from encrypt import vigenere_hill_decrypt

HEADER = 64
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    try:
        print(f"Novo acesso: [{addr}] se conectou!.")

        connected = True
        while connected == True:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                msg = vigenere_hill_decrypt(msg, "chave", [[1, 2], [3, 4]])
                if msg == "!DISCONNECT":
                    connected = False

                print(f"[{addr}]({time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}) {msg}")
                conn.send(f"Mensagem recebida com sucesso! ({time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())})".encode(FORMAT))

    except:
        print(f"Erro com a conexão do cliente [{addr}]({time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())})!")

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Servidor está escutando em: {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[CONEXÕES ATIVAS] {threading.active_count() - 1}")


print("[STARTING] Estabelecendo conexão com servidor!...")
start()