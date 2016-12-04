import asynchat
import asyncore
import socket

debug = True


class Server(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        # Tworzymy gniazdo akceptujące połączenia,
        # Używamy do tego metod create_socket, bind i listen z klasy asyncore.dispatcher
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(('', port))
        self.listen(4)

    def handle_accept(self):
        # zgłasza się nowy klient
        socket, address = self.accept()
        if debug:
            print('Akceptujemy połączenie z adresu {0}'.format(address))
        EchoHandler(socket)


class EchoHandler(asynchat.async_chat):
    ac_in_buffer_size = 8
    ac_out_buffer_size = 8

    def __init__(self, socket, server):
        asynchat.async_chat.__init__(self, socket)
        self.set_terminator(b"\r\n")
        self.data = []

    def collect_incoming_data(self, data):
        if debug:
            print("Inc data:", data)
        self.data.append(data)

    def found_terminator(self):
        data = b''
        for d in self.data:
            data += d
        msg = data.decode('UTF-8')
        if debug:
            print("Instrukcja: " + msg)
        self._process_data(msg)
        self.data = []

    def _process_data(self, msg):
        print(msg)


s = Server('', 12345)
# startujemy pętlą główną
asyncore.loop(5)
