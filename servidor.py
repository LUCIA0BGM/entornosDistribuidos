# servidor.py (escucha en 127.0.0.1:8809 con registro en log.txt)

import socket
import threading
import random
import time
from mesa import Mesa
from restaurante import Restaurante
from datetime import datetime

HOST = '127.0.0.1'
PORT = 8809

# Instanciar el restaurante
restaurante = Restaurante()

# Variables globales
pending_orders = []  # Pedidos en espera
prepared_orders = []  # Pedidos listos en cocina
delivering_orders = []  # Pedidos en reparto

def log_event(evento):
    with open("log.txt", "a") as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {evento}\n")

def handle_client(client_socket):
    addr = client_socket.getpeername()
    log_event(f"Conexión establecida con {addr}")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        message = data.decode()
        log_event(f"Mensaje recibido de {addr}: {message}")

        if message == 'estado_pedido':
            estado = f"Pendientes: {pending_orders}, Listos: {prepared_orders}, En reparto: {delivering_orders}"
            client_socket.sendall(estado.encode())
            log_event(f"Respuesta enviada a {addr}: {estado}")

        elif message == 'recoger_pedido':
            if prepared_orders:
                pedido = prepared_orders.pop(0)
                delivering_orders.append(pedido)
                respuesta = f"Pedido {pedido} recogido"
                client_socket.sendall(respuesta.encode())
                log_event(f"Respuesta enviada a {addr}: {respuesta}")
            else:
                respuesta = "No hay pedidos disponibles"
                client_socket.sendall(respuesta.encode())
                log_event(f"Respuesta enviada a {addr}: {respuesta}")

        elif message.startswith('entregar_pedido'):
            mesa = int(message.split()[1])
            if mesa in delivering_orders:
                delivering_orders.remove(mesa)
                respuesta = f"Pedido entregado en mesa {mesa}"
                client_socket.sendall(respuesta.encode())
                log_event(f"Respuesta enviada a {addr}: {respuesta}")
            else:
                respuesta = f"Mesa {mesa} no está en reparto"
                client_socket.sendall(respuesta.encode())
                log_event(f"Respuesta enviada a {addr}: {respuesta}")

    client_socket.close()
    log_event(f"Conexión cerrada con {addr}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Servidor escuchando en {HOST}:{PORT}")
    log_event(f"Servidor iniciado en {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexión establecida con {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def generate_orders():
    while True:
        table = random.randint(1, len(restaurante.mesas))
        pending_orders.append(table)
        evento = f"Nuevo pedido generado para mesa {table}"
        print(evento)
        log_event(evento)

        time.sleep(random.randint(3, 5))

        if table in pending_orders:
            pending_orders.remove(table)
            prepared_orders.append(table)
            evento = f"Pedido para mesa {table} listo en la cocina"
            print(evento)
            log_event(evento)

if __name__ == '__main__':
    threading.Thread(target=start_server).start()
    threading.Thread(target=generate_orders).start()
