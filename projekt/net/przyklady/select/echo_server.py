#!/usr/bin/env python3.4

import socket
import sys
import threading
import select

lock = threading.Lock()
debug = True


class EchoServer:
    def __init__(self, host, port):
        self.clients = []
        self.open_socket(host, port)

    def open_socket(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)

    def run(self):
        while True:

            # definiujemy tablicę deskryptorów, które podamy do funkcji select w celu nasłuchiwania
            readDescr = [sys.stdin, self.server]

            # funkcja select() ma trzy argumenty, pierwszy z nich: tablica deskryptorów plików, które śledzimy pod kątem operqacji czytania,
            # drugi argument to tablica deskryptorów plików śledzona pod kątem pisania, trzeci argument to deskryptory śledzone pod kątem wyjątków.
            # zwraca trzy tablice zawierające deskryptory gotowe do "odczytu", "zapisu".

            inputready, outputready, exceptready = select.select(readDescr, [], [])

            for descr in inputready:
                if descr == self.server:

                    clientSocket, clientAddr = self.server.accept()
                    if debug:
                        print("Zgłoszenie klienta, adres: {0}".format(clientAddr))

                    lock.acquire()

                    self.clients.append(clientSocket)
                    if debug:
                        self._show_clients()

                    lock.release()
                    Client(clientSocket, clientAddr, self).start()

                elif descr == sys.stdin:
                    dane = "Server:" + sys.stdin.readline()

                    echodata = bytes(dane, "UTF-8")

                    lock.acquire()
                    err = []
                    for clients in self.clients:
                        try:
                            clients.send(echodata)
                        except:
                            err.append(clients)
                    lock.release()
                    for e in err:
                        self.cleanClient(e)

    def _show_clients(self):
        print("Liczba klientów: {0}".format(len(self.clients)))

    def clean_client(self, client):
        if client in self.clients:
            self.clients.remove(client)
            client.close()
            if debug:
                self._show_clients()

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
            try:
                data = self.clientSocket.recv(1024);
                if data:
                    s = data.decode('UTF-8')
                    s = "Echo:" + s
                    echodata = bytes(s, 'UTF-8')

                    lock.acquire()

                    err = []
                    for clients in self.server.clients:
                        try:
                            clients.send(echodata)
                        except:
                            err.append(clients)
                    self.server.clean_clients(err)

                    lock.release()

                else:
                    running = False
                    lock.acquire()
                    self.server.clean_client(self.clientSocket)
                    lock.release()
                    break

            except:
                lock.acquire()
                self.server.clean_client(self.clientSocket)
                lock.release()
                running = False
                break


server = EchoServer('', 12345)
server.run()
