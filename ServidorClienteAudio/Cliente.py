'''
  Cliente capaz de enviar audio a un servidor
  Version 1.0
  Autor: Edgar Soto Avalos
'''
import socket

def send_audio_file(file_path, host, port):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(file_data)
    print(f"Archivo de audio {file_path} enviado exitosamente al servidor.")

# Parámetros de conexión al servidor
host = '127.0.0.1'  # Cambia esto a la dirección IP o nombre de host de tu servidor
port = 12345  # Cambia esto al puerto utilizado por tu servidor

# Ruta del archivo de audio que deseas enviar al servidor
file_path = 'SONG_NAME.x'  # Cambia esto a la ruta de tu archivo de audio y su terminacion

# Llamada a la función para enviar el archivo al servidor
send_audio_file(file_path, host, port)
