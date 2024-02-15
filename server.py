import socket
import threading
import pickle
import random

# Server configuration
HOST = '127.0.0.1'
PORT = 5050

# Create a TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

# Game state
initial_bird_y = 300
bird_width = 40
bird_height = 30
bird_x = 50
bird_y = initial_bird_y
bird_speed = 5
gravity = 0.25
jump_force = -7
pipe_width = 70
pipe_gap = 150
pipe_speed = 3
pipes = []
scores = {}  # Dictionary to store scores for each client

def generate_pipes():
    if len(pipes) == 0 or pipes[-1]['x'] < 400 - pipe_gap * 2:
        pipe_height = random.randint(100, 400 - pipe_gap - 100)
        pipes.append({'x': 400, 'y': pipe_height})

def move_pipes():
    for pipe in pipes:
        pipe['x'] -= pipe_speed

def check_collision():
    global scores
    for client_id, score in scores.items():
        bird_y = score['bird_y']
        for pipe in score['pipes']:
            if bird_x + bird_width > pipe['x'] and bird_x < pipe['x'] + pipe_width:
                if bird_y < pipe['y'] or bird_y + bird_height > pipe['y'] + pipe_gap:
                    scores[client_id]['bird_y'] = initial_bird_y
                    scores[client_id]['pipes'] = []
                    scores[client_id]['score'] = 0

                    # Update high score
                    max_score = max(scores.values(), key=lambda x: x['score'])['score']
                    print("High Score:", max_score)
                    break
            if pipe['x'] + pipe_width < 0:
                scores[client_id]['pipes'].remove(pipe)
                scores[client_id]['score'] += 1
    return False

def handle_client(conn, addr):
    global bird_y
    print(f"[NEW CONNECTION] {addr} connected.")

    # Initialize score for the new client
    client_id = addr
    scores[client_id] = {'bird_y': bird_y, 'pipes': [], 'score': 0}

    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                print(f"[{addr}] disconnected.")
                del scores[client_id]
                break

            if data == "JUMP":
                scores[client_id]['bird_y'] += jump_force

            generate_pipes()
            move_pipes()

            game_state = {'bird_y': scores[client_id]['bird_y'], 'pipes': pipes, 'score': scores[client_id]['score']}
            game_state_data = pickle.dumps(game_state)
            conn.send(game_state_data)

            check_collision()

        except Exception as e:
            print(e)
            break

    conn.close()

def start_server():
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start_server()
