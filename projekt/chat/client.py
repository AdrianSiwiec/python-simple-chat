import queue
import threading
import sys
import time
from commons import MessageType, decode, encode
from socket import *
from view import create_view


class ReceiverThread(threading.Thread):
    def __init__(self, receive_queue):
        super().__init__(daemon=True)
        self.viewInput = receive_queue
        self.running = True

    def run(self):
        while self.running:
            try:
                received = sock.recv(1024)
                msg = decode(received)
                if msg.msg_type == MessageType.PING:
                    pass
                elif msg.msg_type == MessageType.sendMessage:
                    print("Got message")
                    receive_queue.put((msg.message, msg.sender, msg.receiver))
                else:
                    print("Got unrecognized message")

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


def connect_to_server(username):
    accepted = False
    counter = 1
    while not accepted:
        to_send = encode(MessageType.addUsername, username + ("" if counter == 1 else str(counter)))
        sock.send(to_send)
        data = sock.recv(1024)
        print(data)
        msg_type = decode(data).msg_type
        if msg_type != MessageType.OK:
            print("Server didn't accept us, trying other username")
            counter += 1
        else:
            accepted = True

    username += "" if counter == 1 else str(counter)
    return username


if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = "Anon"

send_queue = queue.Queue()
receive_queue = queue.Queue()
view = create_view(send_queue, receive_queue)

senderThread = SenderThread(send_queue)
receiverThread = ReceiverThread(receive_queue)

sock = socket(AF_INET, SOCK_STREAM)  # utworzenie gniazda
sock.connect(('localhost', 12345))  # nawiazanie polaczenia

username = connect_to_server(username)
senderThread.start()
receiverThread.start()

view.start_update_loop()
view.main_loop()
