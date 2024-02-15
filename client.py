import pygame
import socket
import pickle
from main import main 
# Server configuration
SERVER = '127.0.0.1'
PORT = 5050

# Socket initialization
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

# Call the main function to start the game
main()

# Close the socket connection after the game ends
client.close()
