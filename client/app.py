import socket
import os
import threading
import time

class RemoteControlClient():
    IP = "127.0.0.1"
    PORT = 8000
    ADDR = (IP, PORT)
    SIZE = 4096
    DECODING = ""
    FORMAT = "utf-8"
    CONNECTED = False
    FINISH = False

    def create_thread(self, thread_function, args=(), daemon_state=True, start=True):
        new_thread = threading.Thread(target=thread_function, args=args)
        new_thread.daemon = daemon_state
        new_thread.name = thread_function.__name__
        if start:
            new_thread.start()
        return new_thread

    def get_input(self, client):
        while not self.FINISH:
            msg = input()
            if msg == "exit":
                self.CONNECTED = False
                self.FINISH = True
                try:
                    client.send(msg.encode(self.FORMAT))
                    client.close()
                except:
                    print("Client didn't connect to a server.")
                return
            elif msg == "threads":
                print(threading.enumerate())
            else:
                client.send(msg.encode(self.FORMAT, errors='ignore'))
            time.sleep(0.1)

    def get_response(self, client):
        while not self.FINISH:
            msg = client.recv(self.SIZE).decode(self.FORMAT)
            if msg == "disconnected":
                self.CONNECTED = False
                self.FINISH = True
                try:
                    client.send(msg.encode(self.FORMAT))
                    client.close()
                except:
                    print("")
            else:
                print(f'Admin: {msg}')
            time.sleep(0.1)


    def start(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # creating input thread
        self.create_thread(self.get_input, (client,))

        print("Waiting for a connection...")
        while not self.FINISH: 
            if not self.CONNECTED:
                try:
                    client.connect(self.ADDR)
                    print(f"Connected: Client connected to server at {self.IP}:{self.PORT}")
                    client.send(f"Username: {os.getlogin()}".encode(self.FORMAT)) 
                    self.CONNECTED = True
                    self.create_thread(self.get_response, (client,))
                except Exception as e:
                    print(str(e))
            time.sleep(0.1)
            
        print(f"Client disconnected.")


RemoteControlClient().start()