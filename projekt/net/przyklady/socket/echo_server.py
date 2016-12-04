import socket
import sys
import threading

debug = True


class EchoServer:
    def __init__(self, host, port):
        self.clients = []
        self.open_socket(host, port)

    def open_socket(self, host, port):
        """
        Metoda tworząca server, na hoscie: host i porcie: port
        """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)

    def run(self):
        while True:
            clientSocket, clientAddr = self.server.accept()
            if debug:
                print("SERVER LOG: Zgłoszenie klienta, adres: {0}".format(clientAddr))

            self.clients.append(clientSocket)
            if debug:
                self.number_of_clients()

            Client(clientSocket, clientAddr, self).start()

    def number_of_clients(self):
        print("Liczba klientów: {0}".format(len(self.clients)))

    def clean_client(self, client):
        if client in self.clients:
            try:
                self.clients.remove(client)
                client.close()
                if debug:
                    self.number_of_clients()
            except:
                if debug:
                    print("Exception: usuwanie klienta")

    def clean_clients(self, err):
        for client in err:
            self.clean_client(client)


class Client(threading.Thread):
    def __init__(self, clientSocket, clientAddr, server):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket;
        self.clientAddr = clientAddr;
        self.server = server

    def run(self):
        running = True
        while running:
            data = b''
            try:
                data = self.clientSocket.recv(1024);
                if data:
                    s = data.decode('UTF-8')
                    s = "Echo:" + s
                    echodata = bytes(s, 'UTF-8')
                    err = []
                    for clients in self.server.clients:
                        try:
                            clients.send(echodata)
                        except:
                            err.append(clients)
                    self.server.clean_clients(err)


                else:
                    running = False
                    self.server.clean_client(self.clientSocket)
                    if debug:
                        print("IF clause: {0}".format(data))
                    break

            except:
                self.server.clean_client(self.clientSocket)
                running = False
                if debug:
                    print("EXCEPT clasue: {0}".format(data))
                break


server = EchoServer('', 12345)
server.run()
