import socket
import threading
import time

from info import INFO

class Server:
    IP = "0.0.0.0"
    PORT = 8000
    ADDR = (IP, PORT)
    SIZE = 4096
    FORMAT = "utf-8"
    CLIENTS = []
    USERNAMES = []
    FINISH = False


    def create_thread(self, thread_function, args=(), daemon_state=True, start=True):
        new_thread = threading.Thread(target=thread_function, args=args)
        new_thread.daemon = daemon_state
        new_thread.name = thread_function.__name__
        if start:
            new_thread.start()
        return new_thread


    def show_clients(self):
        adrrs = []
        for conn in self.CLIENTS:
            adrrs.append(conn.getpeername())
        print(f"\nActive connections:")
        for i in range(len(self.USERNAMES)):
            print(f"id {i}. {self.USERNAMES[i]} - {adrrs[i]}")


    def send_all(self, msg):
        for conn in self.CLIENTS:
            self.send(conn, msg)


    def send(self, conn, msg):
        conn.send(msg.encode(self.FORMAT, errors='ignore'))


    def get_input(self):
        while not self.FINISH:
            msg = input()
            if msg == 'exit':  # "discon"
                print("Server is closing...")
                if self.CLIENTS:
                    print("Clients disconnecting:")
                self.send_all(msg)
                self.FINISH = True
            elif msg[:4] == 'kick':
                try:
                    conn = self.CLIENTS[int(msg.replace("kick ", ""))]
                    self.send(conn, 'disconnected')
                except:
                    print("You have to enter available [client_id] after 'kick'.")
            elif msg == "close":
                self.FINISH = True
            elif msg == "threads":
                print(f"\nActive threads: {threading.enumerate()}")
            elif msg == "clients":
                self.show_clients()
            elif msg == "help":
                print('\n'.join(INFO))
            elif msg[:4] == '/sa ':
                self.send_all(msg.replace('/sa ', ''))
            else:
                print(f"Incorrect command '{msg}': type 'help' to see all commands")
            time.sleep(0.1)


    def new_client(self, server):
        while not self.FINISH:
            conn, addr = server.accept()      
            self.CLIENTS.append(conn)
            # creating thread that is handling client connection and recieving messages
            self.create_thread(self.handle_client, (conn,))
            time.sleep(0.1)


    def handle_client(self, conn):
        addr = conn.getpeername()

        print(f"\n{self.CLIENTS.index(conn)}. New connection: {addr} connected.")
        try:
            while not self.FINISH:
                answer = conn.recv(self.SIZE).decode(self.FORMAT, errors='ignore')
                if answer == 'discon':
                    break
                elif answer == '':
                    print("Empty answer: there is probably no such command in cmd.")
                elif answer[:8] == 'Username':
                    print(answer)
                    self.USERNAMES.append(answer.replace("Username: ", ""))
                else:
                    print(
                        f"{self.CLIENTS.index(conn)}. User - {self.USERNAMES[self.CLIENTS.index(conn)]} {addr}: {answer}")
                time.sleep(0.1)
        except Exception as e:
            print(str(e))

        print(f"{addr} disconnecting...")
        del self.USERNAMES[self.CLIENTS.index(conn)]
        self.CLIENTS.remove(conn)
        conn.close()


    def main(self):
        print("\nServer is starting...")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(self.ADDR)
        server.listen()
        print(f"Listening: {self.IP}:{self.PORT}")

        self.create_thread(self.new_client, (server,))
        self.create_thread(self.get_input)
        
        x = True  # just for an infinte loop with no output - when the loop finishes, all daemon threads close
        while not self.FINISH:
            x = not x
            time.sleep(0.1)



if __name__ == "__main__":
    Server().main()
