import queue
import threading
import sys
import time
from commons import MessageType, decode, encode
from socket import *
from view import create_view


class ReceiverThread(threading.Thread):
    def __init__(self, receive_queue, add_users_queue):
        super().__init__(daemon=True)
        self.viewInput = receive_queue
        self.running = True
        self.receive_queue = receive_queue
        self.add_users_queue = add_users_queue

    def run(self):
        while self.running:
            try:
                received = sock.recv(1024)
                msg = decode(received)
                print("Received: " + str(msg))
                if msg.msg_type == MessageType.PING:
                    pass
                elif msg.msg_type == MessageType.sendMessage:
                    print("Got message")
                    self.receive_queue.put((msg.message, msg.sender, msg.receiver))
                elif msg.msg_type == MessageType.addUsername:
                    print("Got username to add: " + msg.sender)
                    self.add_users_queue.put((True, msg.sender))
                elif msg.msg_type == MessageType.removeUsername:
                    self.add_users_queue.put((False, msg.sender))
                else:
                    print("Got unrecognized message: " + str(msg.msg_type))

            except Exception as e:
                print("Receiver Exception: " + str(e))


class SenderThread(threading.Thread):
    def __init__(self, message_queue):
        super().__init__(daemon=True)
        self.message_queue = message_queue
        self.running = True

    def run(self):
        while self.running:
            try:
                to_send, receiver = self.message_queue.get(block=True)
                sock.send(encode(MessageType.sendMessage, username, to_send, receiver))
            except Exception as e:
                print("Sender Exception: " + str(e))


def connect_to_server(username, add_user_queue):
    accepted = False
    counter = 1
    while not accepted:
        to_send = encode(MessageType.addUsername, username + ("" if counter == 1 else str(counter)))
        sock.send(to_send)
        data = False
        while not data:
            data = sock.recv(1024)
        print(data)
        msg = decode(data)
        msg_type = msg.msg_type
        if msg_type == MessageType.usernameTaken:
            print("Server didn't accept us, trying other username")
            counter += 1
        elif msg_type == MessageType.OK:
            print("Server accepted")
            accepted = True
        elif msg_type == MessageType.addUsername:
            add_users_queue.put(True, msg.sender)

    username += "" if counter == 1 else str(counter)
    return username


if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = "Anon"

send_queue = queue.Queue()
receive_queue = queue.Queue()
add_users_queue = queue.Queue()
view = create_view(send_queue, receive_queue, add_users_queue)

senderThread = SenderThread(send_queue)
receiverThread = ReceiverThread(receive_queue, add_users_queue)

sock = socket(AF_INET, SOCK_STREAM)  # utworzenie gniazda
sock.connect(('localhost', 12345))  # nawiazanie polaczenia

username = connect_to_server(username, add_users_queue)
senderThread.start()
receiverThread.start()

view.start_update_loop()
view.main_loop()
