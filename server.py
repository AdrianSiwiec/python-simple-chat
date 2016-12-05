import queue
import socket
import sys
import threading

import time

from commons import decode, MessageType, encode, Message


_debug = True
PORT = 12345


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
            if _debug: print("Zgłoszenie klienta, adres: {0}".format(clientAddr))

            if _debug: self.number_of_clients()

            message_queue = queue.Queue()
            running_queue = queue.Queue()
            running_queue.put(42)  # when running_queue is empty should shut down. It's thread-safe ofc.
            client_to_send = ClientToSend(clientSocket, clientAddr, self, message_queue, running_queue)
            client_to_send.start()
            ClientToReceive(clientSocket, clientAddr, self, message_queue, running_queue).start()
            self.clients.append(clientSocket)
            self.senders.append(client_to_send)

    def number_of_clients(self):
        if _debug: print("Liczba klientów: {0}, {1}".format(len(self.clients), len(self.senders)))

    def clean_client(self, client):
        username = ""
        for s in self.senders:
            if s.clientSocket == client:
                self.senders.remove(s)
                username = s.username
        if _debug: print("Server removed user: " + username)
        for s in self.senders:
            if s.clientSocket != client:
                s.messages_to_receive.put(Message(MessageType.removeUsername, username))
        if client in self.clients:
            try:
                self.clients.remove(client)
                client.close()
                if _debug: self.number_of_clients()
            except:
                if _debug: print("Exception: usuwanie klienta")

    def clean_clients(self, err):
        for client in err:
            self.clean_client(client)


class ClientToSend(threading.Thread):
    def __init__(self, clientSocket, clientAddr, server, messages_to_receive, running_queue):
        threading.Thread.__init__(self, daemon=True)
        self.clientSocket = clientSocket
        self.clientAddr = clientAddr
        self.server = server
        self.username = "default"  # when you see it on client side, somethings wrong. Should appear in logs at start
        self.messages_to_receive = messages_to_receive
        self.running_queue = running_queue

    def run(self):
        while not self.running_queue.empty():
            data = b''
            try:
                msg = self.messages_to_receive.get(block=True)
                if _debug: print(self.username + ": got: " + str(msg))
                if msg.msg_type == MessageType.addUsername:
                    self.clientSocket.send(encode(MessageType.addUsername, msg.sender, msg.message, msg.receiver))
                elif msg.msg_type == MessageType.removeUsername:
                    self.clientSocket.send(encode(MessageType.removeUsername, msg.sender))
                elif msg.msg_type == MessageType.sendMessage:
                    self.clientSocket.send(encode(MessageType.sendMessage, msg.sender, msg.message, msg.receiver))
                elif msg.msg_type == MessageType.usernameTaken:
                    self.clientSocket.send(encode(MessageType.usernameTaken))
                elif msg.msg_type == MessageType.OK:
                    self.username = msg.sender
                    self.clientSocket.send(encode(MessageType.OK))
                else:
                    if _debug: print("Unrecognized message: " + str(msg))

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
                if _debug: print("EXCEPT clause: {0}".format(data))
                break


class ClientToReceive(threading.Thread):  # receives from socket, puts actions to queue for senders
    def __init__(self, client_socket, client_addr, server, queue_to_fill, running_queue):
        threading.Thread.__init__(self, daemon=True)
        self.client_socket = client_socket
        self.client_addr = client_addr
        self.server = server
        self.running_queue = running_queue
        self.queue_to_fill = queue_to_fill

    def run(self):
        while not self.running_queue.empty():
            try:
                received_data = self.client_socket.recv(1024)
                if received_data:
                    received_data = received_data.decode('UTF-8').split("$")
                    if _debug: print("Server received raw data: " + str(received_data))
                    for data in received_data:
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
                                    if _debug: print("Server didn't accept user: " + msg.sender)
                                    self.queue_to_fill.put(Message(MessageType.usernameTaken))
                                else:
                                    if _debug: print("Server accepted user: " + msg.sender)
                                    self.queue_to_fill.put(Message(MessageType.OK, msg.sender))
                                    for s in self.server.senders:
                                        if s.username != msg.sender and s.username != "default":
                                            s.messages_to_receive.put(msg)
                                            self.queue_to_fill.put(Message(MessageType.addUsername, s.username))

                else:
                    self.running_queue.get()
                    self.server.clean_client(self.client_socket)
                    if _debug: print("IF clause: {0}".format(received_data))
                    break

            except Exception as e:
                self.server.clean_client(self.client_socket)
                self.running_queue.get()
                if _debug: print("EXCEPT clasue: {0}".format(e))
                break


server = EchoServer('', PORT)
server.run()
