'''
    Servidor con el juego de memorama
    Version 3.0
    Autor: Soto Avalos Edgar
'''

'''
    Importamos las bibliotecas
'''
import socket
import random
import time

'''DEFINIMOS LA LISTA DE NUMEROS MEDIANTE LA CUAL SE IRA LLENANDO LA MATRIZ'''
NUMEROS_4X4 = list(range(1, 9)) * 2
NUMEROS_6X6 = list(range(1, 19)) * 2

'''Funcion Main'''
HOST = "127.0.0.1"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024

def juego_incio():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.bind((HOST, PORT))
        TCPServerSocket.listen()
        print("El servidor TCP está disponible y en espera de solicitudes")
        Client_conn, Client_addr = TCPServerSocket.accept()
        with Client_conn:
            print("Conectado a", Client_addr)
            tiempo_inicio = time.time()
            Client_conn.sendall(bytes('Bienvenido al Juego de Memoria\nSelecciona la dificultad:\n1. 4x4\n2. 6x6\nIngresa tu seleccion (1 o 2):','utf-8'))
            '''HOY'''
            while True:
                print("Esperando a recibir datos... ")
                data = Client_conn.recv(buffer_size)
                choice = data.decode()
                print("Recibido,", choice, "   de ", Client_addr)
                if choice == '1':
                    fils, cols = 4, 4
                    break
                elif choice == '2':
                    fils, cols = 6, 6
                    break
                else:
                    Client_conn.sendall(bytes("Entrada invalida.Ingresa de nuevo la dificultad\n", 'utf-8'))
            matriz = crear_matriz(fils, cols)
            ciega = matriz_ciega(fils,cols)
            pts_usr = 0
            pts_pc = 0
            juego = 0
            imp_matriz(matriz)
            # PREGUNTAMOS POR LAS COORDENADAS
            while True:

                '''Codigo donde pedimos al usuario los valores del numero y verificamos si son validos'''
                while True:
                    Client_conn.sendall(bytes('Ingresa la fila del primer numero (0-3)', 'utf-8'))
                    f1 = Client_conn.recv(buffer_size)
                    fils1 = int(f1.decode())
                    if (fils1 <= 3 and fils1 >= 0):
                        print("Me llego la fila del primer numero", fils1)
                        break
                    else:
                        Client_conn.sendall(bytes('Valor no valido', 'utf-8'))
                while True:
                    Client_conn.sendall(bytes('Ingresa la columna del primer numero (0-3)', 'utf-8'))
                    c1 = Client_conn.recv(buffer_size)
                    col1 = int(c1.decode())
                    if(col1 <=3 and col1 >= 0):
                        print("Me llego la columa del primer numero (0-3)", col1)
                        break
                    else:
                        Client_conn.sendall(bytes('Valor no valido', 'utf-8'))
                num1 = matriz[fils1][col1]
                print("Num1 ", {num1})
                '''Se ingresa columna y fila del segundo numero'''
                while True:
                    Client_conn.sendall(bytes('Ingresa la fila del segundo numero (0-3)', 'utf-8'))
                    f2 = Client_conn.recv(buffer_size)
                    fils2 = int(f2.decode())
                    if (fils2 <=3 and fils2 >=0):
                        print("Me llego la fila del segundo numero", fils2)
                        break
                    else:
                        Client_conn.sendall(bytes('Valor no valido', 'utf-8'))
                while True:
                    Client_conn.sendall(bytes('Ingresa la columna del segundo numero(0-3)', 'utf-8'))
                    c2 = Client_conn.recv(buffer_size)
                    col2 = int(c2.decode())
                    if (col2 <=3 and col2 >=0):
                        print("Me llego la columna del segundo numero",col2)
                        break
                    else:
                        Client_conn.sendall(bytes('Valor no valido', 'utf-8'))
                num2 = matriz[fils2][col2]
                print("Num2 ", {num2})
                if num1 == num2 and (fils1 != fils2 or col1 != col2):
                    aux = str(num1)
                    Client_conn.sendall(bytes("El numero que encontraste es:"+aux,'utf-8'))
                    Client_conn.sendall(bytes("\nCoincidencia encontrada!\n", 'utf-8'))
                    ciega[fils1][col1] = num1
                    ciega[fils2][col2] = num2
                    juego += 1
                    #Convertimos la matriz en cadena para poder enviarla al cliente
                    ciega_str = '\n'.join([' '.join([str(num) for num in row]) for row in ciega])
                    Client_conn.sendall(bytes(ciega_str+"\n", 'utf-8'))
                    pts_usr += 1
                else:
                    aux = str(num1)
                    aux1 = str(num2)
                    Client_conn.sendall(bytes("El numero que encontraste es:" + aux + " y " + aux1, 'utf-8'))
                    Client_conn.sendall(bytes("No coinciden sera turno del computador\n", 'utf-8'))
                    computer_row1, computer_col1 = random.randint(0, fils - 1), random.randint(0, cols - 1)
                    computer_num1 = matriz[computer_row1][computer_col1]
                    computer_row2, computer_col2 = random.randint(0, fils - 1), random.randint(0, cols - 1)
                    computer_num2 = matriz[computer_row2][computer_col2]
                    print("Los dos numeros escogidos por el computador fueron ", computer_num1, "en las cordeenadas",
                          computer_row1, computer_col1, "y", computer_num2, "en las corrdenadas", computer_row2,
                          computer_col2)

                    # VEMOS SI LOS NUMEROS ESCOGIDOS POR EL COMPUTADOR SON IGUALES
                    if computer_num1 == computer_num2 and (
                            computer_row1 != computer_row2 or computer_col1 != computer_col2):
                        Client_conn.sendall(bytes("El servidor encontro un par.\n", 'utf-8'))
                        juego += 1
                        pts_pc += 1
                        ciega[fils1][col1] = num1
                        ciega[fils2][col2] = num2
                        ciega_str = '\n'.join([' '.join([str(num) for num in row]) for row in ciega])
                        Client_conn.sendall(bytes(ciega_str + "\n", 'utf-8'))
                    else:
                        Client_conn.sendall(bytes("El servidor no encontro coincidendia\n", 'utf-8'))
                par=str(juego)
                print("Pares encontrados"+par)
                if juego == (fils * cols) / 2:
                    Client_conn.sendall(bytes("Juego Terminado",'utf-8'))
                    ciega_str = '\n'.join([' '.join([str(num) for num in row]) for row in ciega])
                    Client_conn.sendall(bytes(ciega_str + "\n", 'utf-8'))
                    break

'''Funcion para imprimir la matriz'''
def imp_matriz(matriz):
    for fils in matriz:
        for num in fils:
            print(num, end=' ')
        print()
'''Funcion para crear la matriz'''
def crear_matriz(fils, cols):
    if fils == 4 and cols == 4:
        numeros = NUMEROS_4X4
    elif fils == 6 and cols == 6:
        numeros = NUMEROS_6X6
    else:
        raise ValueError("Tamaño de Matriz Invalido OCURRIO UN ERROR.")
    # CREAMOS LA MATRIZ
    matriz = [[0 for j in range(cols)] for i in range(fils)]
    for i in range(fils):
        for j in range(cols):
            num = random.choice(numeros)
            matriz[i][j] = num
            numeros.remove(num)
    return matriz

'''Funcion para crear la matriz tablero para el cliente'''
def matriz_ciega(fils,cols):
    matriz_ciega = [[0 for j in range(cols)] for i in range(fils)]
    for i in range(fils):
        for j in range(cols):
            eq = 'x'
            matriz_ciega[i][j] = eq
    return matriz_ciega
'''Se llama a la funcion inicio'''
juego_incio()
