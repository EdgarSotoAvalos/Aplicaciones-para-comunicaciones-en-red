'''
  Servidor capaz de recivir audio de uno o varios clientes
  Version 1.0
  Autor:Edgar Soto Avalos
'''
import selectors
import socket

# Crear un objeto Selector
sel = selectors.DefaultSelector()

# Configurar la dirección IP y el puerto del servidor
host = '172.100.92.62'  # Dirección IP del servidor
port = 12345 # Puerto del servidor

# Crear un socket TCP y configurarlo como no bloqueante
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setblocking(False)

# Enlazar el socket a la dirección IP y el puerto del servidor
server_socket.bind((host, port))

# Escuchar conexiones entrantes
server_socket.listen()
print("El servidor esta escuchando")
# Registrar el socket en el Selector para eventos de lectura
sel.register(server_socket, selectors.EVENT_READ, data=None)

def accept_connection(sock):
    # Aceptar una nueva conexión de cliente
    client_socket, client_address = sock.accept()
    print(f'Cliente conectado desde {client_address[0]}:{client_address[1]}')
    # Configurar el socket del cliente como no bloqueante
    client_socket.setblocking(False)
    # Registrar el socket del cliente en el Selector para eventos de lectura
    sel.register(client_socket, selectors.EVENT_READ, data=client_address)

def receive_audio_file(sock, addr):
    # Recibir datos del cliente
    data = sock.recv(4096)
    if data:
        # Guardar los datos recibidos en un archivo de audio
        file_name = f'audio_{addr[0]}_{addr[1]}.mp3'
        with open(file_name, 'ab') as f:
            f.write(data)
    else:
        # Si no se reciben datos, cerrar la conexión del cliente
        print(f'Archivo de audio recibido desde {addr[0]}:{addr[1]}')
        sel.unregister(sock)
        sock.close()

# Bucle principal del servidor
while True:
    # Esperar a que ocurran eventos en el Selector
    events = sel.select()
    for key, mask in events:
        # Si el evento es una nueva conexión entrante
        if key.data is None:
            accept_connection(key.fileobj)
        else:
            # Si el evento es una lectura de datos del cliente
            receive_audio_file(key.fileobj, key.data)
