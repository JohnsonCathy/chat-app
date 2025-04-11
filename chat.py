import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading
import sys

# Server configuration
HOST = '127.0.0.1'  # Server IP address
PORT = 5000        # Server port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Global variables
username = ""
message_entry = None
send_button = None
window = None 

# Function to receive messages from the server
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Display the incoming message in the chat window
                chat_window.config(state=tk.NORMAL)  # Enable editing the chat window
                chat_window.insert(tk.END, message + "\n")
                chat_window.yview(tk.END)  # Scroll to the bottom
                chat_window.config(state=tk.DISABLED)  # Disable editing
            else:
                # If message is empty, it indicates the server has disconnected
                raise Exception("Server has disconnected.")
        except Exception as e:
            print(f"Error receiving message: {e}")
            handle_disconnect()
            break

# Function to handle username input and start chat
def set_username():
    global username, send_button  # Make send_button and username global
    username = username_entry.get()  # Get username from entry box
    if username:
        # Disable the username entry and start the chat
        username_entry.config(state=tk.DISABLED)
        username_label.config(text=f"Welcome, {username}!")  # Show a welcome message
        message_entry.config(state=tk.NORMAL)  # Enable message entry
        send_button.config(state=tk.NORMAL)  # Enable the send button
        # Send username to the server
        try:
            client_socket.send(username.encode('utf-8'))
        except:
            handle_disconnect()

# Function to handle client-side connection and setup the chat UI
def start_client():
    global username, message_entry, username_entry, username_label, send_button, window

    try:
        client_socket.connect((HOST, PORT))
        print("Connected to server!")

        # Create the Tkinter window for the UI
        window = tk.Tk()
        window.title("Chat Application")

        # Create a scrolled text box for the chat area
        global chat_window
        chat_window = scrolledtext.ScrolledText(window, width=50, height=15, wrap=tk.WORD, state=tk.DISABLED)
        chat_window.grid(row=0, column=0, padx=10, pady=10)

        # Entry widget for user to input message
        message_entry = tk.Entry(window, width=50, state=tk.DISABLED)  # Initially disabled
        message_entry.grid(row=1, column=0, padx=10, pady=5)

        # Send button to send the message
        send_button = tk.Button(window, text="Send", width=20, state=tk.DISABLED, command=send_message)  # Initially disabled
        send_button.grid(row=1, column=1, padx=10, pady=5)

        # Label for username input
        username_label = tk.Label(window, text="Enter your name:")
        username_label.grid(row=2, column=0, padx=10, pady=10)

        # Entry widget for username
        username_entry = tk.Entry(window, width=50)
        username_entry.grid(row=3, column=0, padx=10, pady=5)

        # Submit button for username
        submit_button = tk.Button(window, text="Submit", width=20, command=set_username)
        submit_button.grid(row=3, column=1, padx=10, pady=5)

        # Focus on username entry field
        username_entry.focus()

        # Start a separate thread to receive incoming messages
        threading.Thread(target=receive_messages, daemon=True).start()

        # Start the main loop for chat window
        window.mainloop()

    except Exception as e:
        print(f"Error: {e}")
        client_socket.close()
        sys.exit()

# Function to send messages to the server
def send_message():
    message = message_entry.get()  # Get the text from the message entry box
    if message:
        formatted_message = f"{message}"
        try:
            client_socket.send(formatted_message.encode('utf-8'))  # Send message to server
            message_entry.delete(0, tk.END)  # Clear the message entry box after sending
        except Exception as e:
            print(f"Error sending message: {e}")
            handle_disconnect()

# Function to handle server disconnection or error
def handle_disconnect():
    # Close the socket and window
    client_socket.close()
    window.quit() 

if __name__ == "__main__":
    start_client()