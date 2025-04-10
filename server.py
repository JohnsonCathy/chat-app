import socket
import threading

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 12345       # Port to listen on

# List to maintain active connections
clients = []

# Handle communication with a single client
def handle_client(client_socket, client_address):
    try:
        name = client_socket.recv(1024).decode("utf-8")  # Receive the user's name
        print(f"{name} joined the chat.")

        # Send welcome message to the client
        client_socket.send(f"Welcome {name} to the chat!".encode('utf-8'))
        
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break  # Client disconnected

            print(f"{name}: {message}")  # Log message on server

            # Broadcast the message to all other clients
            broadcast_message(f"{name}: {message}", client_socket)

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        # Remove client from the active list and close the connection
        clients.remove(client_socket)
        client_socket.close()
        print(f"{client_address} disconnected.")

# Broadcast message to all connected clients except the sender
def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # In case of error, remove the client
                clients.remove(client)

# Main server loop
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)  # Max number of queued connections

    print(f"Server started on {HOST}:{PORT}")

    while True:
        connection_socket, client_address = server_socket.accept()
        clients.append(connection_socket)
        
        # Prompt for the user's name
        connection_socket.send("Enter your name:".encode('utf-8'))
        threading.Thread(target=handle_client, args=(connection_socket, client_address)).start()

if __name__ == "__main__":
    start_server()
