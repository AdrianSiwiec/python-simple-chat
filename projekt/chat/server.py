import queue
import socket
import sys
import threading

from commons import decode, MessageType, encode

debug = True


class EchoServer:
    def __init__(self, host, port):
        self.clients = []
        self.senders = []
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

            if debug:
                self.number_of_clients()

            message_queue = queue.Queue()
            running_queue = queue.Queue()
            running_queue.put(42)
            client_to_send = ClientToSend(clientSocket, clientAddr, self, message_queue, running_queue)
            client_to_send.start()
            ClientToReceive(clientSocket, clientAddr, self, running_queue, message_queue).start()
            self.clients.append(clientSocket)
            self.senders.append(client_to_send)

    def number_of_clients(self):
        print("Liczba klientów: {0}".format(len(self.clients)))

    def clean_client(self, client):
        for s in self.senders:
            if s.server == client:
                self.senders.remove(s)
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


class ClientToSend(threading.Thread):
    def __init__(self, clientSocket, clientAddr, server, messages_to_receive, running_queue):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
        self.server = server
        self.username = "Anon"
        self.messages_to_receive = messages_to_receive
        self.running_queue = running_queue

    def run(self):
        while not self.running_queue.empty():
            data = b''
            try:
                msg = self.messages_to_receive.get(block=True)
                if msg.msg_type == MessageType.addUsername:
                    self.username = msg
                    self.clientSocket.send(encode(MessageType.OK))
                elif msg.msg_type == MessageType.sendMessage:
                    self.clientSocket.send(encode(MessageType.sendMessage, msg.sender, msg.message, msg.receiver))
                elif msg.msg_type == MessageType.usernameTaken:
                    self.clientSocket.send(encode(MessageType.usernameTaken))
                else:
                    print("Unrecognized message: " + str(msg["msg_type"]) + "#" + str(msg))

                echodata = encode(MessageType.PING)
                err = []
                for clients in self.server.clients:
                    try:
                        clients.send(echodata)
                    except:
                        err.append(clients)
                self.server.clean_clients(err)

            except:
                self.server.clean_client(self.clientSocket)
                self.running_queue.get()
                if debug:
                    print("EXCEPT clasue: {0}".format(data))
                break


class ClientToReceive(threading.Thread):
    def __init__(self, client_socket, client_addr, server, running_queue, queue_to_fill):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_addr = client_addr
        self.server = server
        self.running_queue = running_queue
        self.queue_to_fill = queue_to_fill

    def run(self):
        while not self.running_queue.empty():
            data = b''
            try:
                data = self.client_socket.recv(1024)
                if data:
                    msg = decode(data)
                    if msg.msg_type == MessageType.sendMessage:
                        for s in self.server.senders:
                            if msg.receiver == "ALL" or msg.receiver == s.username:
                                s.messages_to_receive.put(msg)

                    elif msg.msg_type == MessageType.addUsername:
                        contains = False
                        for s in self.server.senders:
                            if msg.sender == s.username:
                                contains = True
                        if contains:
                            self.queue_to_fill.put(encode(MessageType.usernameTaken))
                        else:
                            self.queue_to_fill.put(msg)


                else:
                    self.running_queue.get()
                    self.server.clean_client(self.client_socket)
                    if debug:
                        print("IF clause: {0}".format(data))
                    break

            except:
                self.server.clean_client(self.client_socket)
                self.running_queue.get()
                if debug:
                    print("EXCEPT clasue: {0}".format(data))
                break


server = EchoServer('', 12345)
server.run()
