from enum import Enum


class MessageType(Enum):
    OK = 0
    PING = 1
    usernameTaken = 2
    addUsername = 10
    sendMessage = 11


class Message():
    def __init__(self, msg_type, sender="", message="", receiver=""):
        self.msg_type = msg_type
        self.sender = sender
        self.message = message
        self.receiver = receiver

    def encode(self):
        data = str(self.msg_type.value) + "#" + self.sender + "#" + self.message + "#" + self.receiver
        return bytes(data, 'UTF-8')


def decode(message):
    data = message.decode('UTF-8').split("#", 4)
    msg_type = MessageType(int(data[0]))
    sender = data[1]
    message = data[2]
    receiver = data[3]
    return Message(msg_type, sender, message, receiver)


def encode(msg_type, sender="", message="", receiver=""):
    return Message(msg_type, sender, message, receiver).encode()
