import queue
import threading
import sys
from commons import MessageType, decode, encode
from socket import *
from view import create_view

PORT = 12345
ADDRESS = 'localhost'
_debug = True

class ReceiverThread(threading.Thread):
    def __init__(self, receive_queue, add_users_queue, running_queue):
        super().__init__(daemon=True)
        self.viewInput = receive_queue
        self.running = True
        self.receive_queue = receive_queue
        self.add_users_queue = add_users_queue
        self.running_queue = running_queue

    def run(self):
        counter = 0  # counts socket errors in row
        while not self.running_queue.empty():
            try:
                received_data = sock.recv(1024)
                if _debug: print("Received: " + str(received_data) + ": " )
                if not received_data or len(received_data) == 0:
                    counter += 1
                    if counter > 10:
                        raise Exception("Connection Lost")
                    continue
                counter = 0
                received_data = list(map(decode, received_data.decode('UTF-8').split('$')[:-1]))
                for msg in received_data:
                    if _debug: print("Processing: " + str(msg))
                    if msg.msg_type == MessageType.PING:
                        pass
                    elif msg.msg_type == MessageType.sendMessage:
                        self.receive_queue.put((msg.message, msg.sender, msg.receiver))
                    elif msg.msg_type == MessageType.addUsername:
                        self.add_users_queue.put((True, msg.sender))
                    elif msg.msg_type == MessageType.removeUsername:
                        self.add_users_queue.put((False, msg.sender))
                    else:
                        if _debug: print("Got unrecognized message: " + str(msg.msg_type))

            except Exception as e:
                if _debug: print("Receiver Exception: " + str(e))
                self.running_queue.get()


class SenderThread(threading.Thread):
    def __init__(self, message_queue, running_queue):
        super().__init__(daemon=True)
        self.message_queue = message_queue
        self.running = True
        self.running_queue = running_queue

    def run(self):
        while not self.running_queue.empty():
            try:
                to_send, receiver = self.message_queue.get(block=True)
                to = encode(MessageType.sendMessage, username, to_send, receiver)
                if _debug: print("Sending: " + str(to))
                sock.send(to)
            except Exception as e:
                if _debug: print("Sender Exception: " + str(e))
                running_queue.get()


def connect_to_server(username, add_users_queue):  # tries : username, username2, username3 ... until server accepts
    accepted = False
    counter = 1
    while not accepted:
        to_send = encode(MessageType.addUsername, username + ("" if counter == 1 else str(counter)))
        sock.send(to_send)
        received_data = sock.recv(1024)
        received_data = list(map(decode, received_data.decode('UTF-8').split('$')[:-1]))
        for msg in received_data:
            msg_type = msg.msg_type
            if msg_type == MessageType.usernameTaken:
                if _debug: print("Server didn't accept us, trying other username")
                counter += 1
            elif msg_type == MessageType.OK:
                if _debug: print("Server accepted")
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
running_queue = queue.Queue()  # like in server
running_queue.put(42)
view = create_view(send_queue, receive_queue, add_users_queue, running_queue)

senderThread = SenderThread(send_queue, running_queue)
receiverThread = ReceiverThread(receive_queue, add_users_queue, running_queue)

sock = socket(AF_INET, SOCK_STREAM)  # utworzenie gniazda
sock.connect((ADDRESS, PORT))  # nawiazanie polaczenia

username = connect_to_server(username, add_users_queue)
senderThread.start()
receiverThread.start()

view.start_update_loop()
view.main_loop()
