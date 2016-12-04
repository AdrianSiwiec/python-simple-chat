from socket import *

debug = True

s = socket(AF_INET, SOCK_STREAM)  # utworzenie gniazda
s.connect(('localhost', 12345))  # nawiazanie polaczenia

i = 0
running = True
while running:
    try:
        dane = "Dane " + str(i)
        if dane:
            s.send(bytes(dane, 'UTF-8'))
            echodane = s.recv(1024)
        else:
            running = False
            s.close()
        if debug:
            print("{0}".format(echodane.decode('UTF-8')))

        i += 1
    except:
        running = False
        s.close()
