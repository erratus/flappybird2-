import socket
import threading
import pygame

# Server configuration
HOST = '127.0.0.1'
PORT = 5050

# Create a TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

# Game state variables
clients_ready = 0
bird_positions = {}

def handle_client(conn, addr):
    global clients_ready, bird_positions

    while True:
        try:
            bird_y = int(conn.recv(1024).decode())
            ready = conn.recv(1024).decode()
            bird_positions[addr] = bird_y

            if ready == "y":
                clients_ready += 1

            if clients_ready == len(bird_positions):
                # All clients are ready, send instruction to start the game
                for client_conn in clients:
                    client_conn.send("START".encode())

        except Exception as e:
            print(e)
            break

    conn.close()

def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")
    
    
    
    
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {len(clients)}")

# Start the server
if __name__ == "__main__":
    clients = []
    start_server()
