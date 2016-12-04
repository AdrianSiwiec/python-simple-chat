import asyncore, socket

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


class EchoHandler(asyncore.dispatcher):
    def __init__(self, socket):
        asyncore.dispatcher.__init__(self, socket)
        self.data = bytes('', 'UTF-8')
        if debug:
            print(type(self.data))

    def handle_read(self):
        # są dane do czytania
        if debug:
            print("Czytamy ...")
        self.data = self.recv(1024)
        self.data = bytes(("Echo:" + self.data.decode('UTF-8')), 'UTF-8')

    def handle_close(self):
        # zamknięto gniazdo klienta, my też się zamykamy
        if debug:
            print("Zamykamy gniazdo ...")
        self.close()

    def handle_write(self):
        # są dane do zapisu
        if debug:
            print("Piszemy ...")
        self.send(self.data)
        self.data = bytes('', 'UTF-8')

    def writable(self):
        # Ta metoda wykonywana jest za kazdym obiegiem petli loop().
        # Jeżeli zwracamy True, obserwujemy deskryptor gniazda pod
        # kątem operacji pisania

        if (self.data):
            if debug:
                print("Ustawiamy writable na True ...")
            return True
        else:
            if debug:
                print("Ustawiamy writable na False ...")
            return False

    def readable(self):
        # Jak wyżej. Jezeli zwracamy TRUE, obserwujemy
        # deskryptor gniazda pod kątem operacji czytania
        if debug:
            print("Ustawiamy readable na True ...")
        return True


s = Server('', 12346)
# startujemy pętlą główną
asyncore.loop(5)
