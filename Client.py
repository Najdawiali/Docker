import socket
import json
import tkinter as tk

# Predefined server address and port
HOST = 'localhost'
PORT = 5000

def connect_to_server():
    global server_socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((HOST, PORT))
        connect_button.config(text='Connected', state='disabled')
        search_entry.pack(padx=10, pady=10)  # Show the search bar
        search_button.pack(padx=10, pady=10)  # Show the search button
    except ConnectionError as e:
        error_label.config(text=str(e))

def search_word(word):
    request = {'word': word}
    request_json = json.dumps(request)
    server_socket.sendall(request_json.encode())

    data = server_socket.recv(1024).decode()
    response = json.loads(data)
    if 'meaning' in response:
        meaning_label.config(text=response['meaning'])
    else:
        error_label.config(text=response['error'])

window = tk.Tk()
window.title("Dictionary Client")

# Server address display
server_address_label = tk.Label(window, text=f"Server Address: {HOST}:{PORT}")
server_address_label.pack(side=tk.LEFT, padx=10, pady=10)

# Connect button
connect_button = tk.Button(window, text="Connect", command=connect_to_server)
connect_button.pack(side=tk.LEFT, padx=10, pady=10)

# Search functionality (hidden until connected)
search_entry = tk.Entry(window)
search_button = tk.Button(window, text="Search", command=lambda: search_word(search_entry.get()))

meaning_label = tk.Label(window, text="")
meaning_label.pack(pady=10)

error_label = tk.Label(window, text="")
error_label.pack(pady=10)

window.mainloop()