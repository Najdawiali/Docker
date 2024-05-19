import socket
import threading
import json

DIC = "dictionary.txt"


def load_dictionary():
    dictionary = {}
    with open(DIC, 'r') as f:
        for line in f:
            word, meaning = line.strip().split(':')
            dictionary[word] = meaning
    return dictionary


def handle_client(conn, addr, dictionary):
    print(f'Connected by {addr}')
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                break

            request = json.loads(data)
            word = request['word']
            meaning = dictionary.get(word)

            if meaning:
                response = {'meaning': meaning}
            else:
                response = {'error': f"Word '{word}' not found in the dictionary."}

                # here
            response_json = json.dumps(response).encode()
            conn.sendall(response_json)

        except Exception as e:
            print(f'Error handling client {addr}: {e}')
            break
    conn.close()
    print(f'Client {addr} disconnected')  # look here


def main():
    dictionary = load_dictionary()
    HOST = '0.0.0.0'
    PORT = 42
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Client connected from {addr}")
        worker = threading.Thread(target=handle_client, args=(conn, addr, dictionary))
        worker.start()


if _name_ == '_main_':
    main()