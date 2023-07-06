'''
    Cliente para conectarse al servidor con el juego del Memorama
    Version 1.0
    Autor: Soto Avalos Edgar
'''


import socket
import select
import time
#HOST = '127.0.0.1'
#PORT = 65432

ACK_TEXT = 'text_received'


def main():
    #Se instancea el socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #print('socket listo para conectarse')

    # conectarse
    connectionSuccessful = False
    while not connectionSuccessful:
        try:
            sock.connect((HOST, PORT))
            print('conectado al servidor')
            connectionSuccessful = True
            tiempo_inicio = time.time()
        except:
            pass
        # end try
    # end while

    socks = [sock]
    while True:
        readySocks, _, _ = select.select(socks, [], [], 5) #Linea de codigo que espera a que algun socket se conecte

        for sock in readySocks:
            message = receiveTextViaSocket(sock)
            msg1 = str(message)
            if (msg1 == 'None'):
                break
            if (msg1 == 'Juego Terminado'):
                print(msg1 + "\n")
                sock.close()
                tiempo_final = time.time()
                ttotal = tiempo_final - tiempo_inicio
                print(f"La conexion duro: {ttotal:.2f} segundos")
                exit()
            else:
                print(msg1 + "\n")
        msg = input()
        sock.sendall(msg.encode())

def receiveTextViaSocket(sock):
    encodedMessage = sock.recv(1024)
    if not encodedMessage:
        return None
    message = encodedMessage.decode('utf-8')
    return message

if __name__ == '__main__':
    HOST = input("Ingresa la IP a la que te quieres conectar")
    po = input("Ingresa el puerto a la que te quieres conectar")
    PORT = int(po)
    main()
