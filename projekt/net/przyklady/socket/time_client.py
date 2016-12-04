from socket import *

s = socket(AF_INET, SOCK_STREAM)

#nawiazanie polaczenia z serwerem
s.connect(('localhost', 12345)) 

#odbieramy dane, maksimum 1024 bajty
tm = s.recv(1024) 

#konwersja bajtów na string, string jest kodowany w UTF-8
curr_time = tm.decode('UTF-8')

#zamkniecie polaczenia
s.close()

print('Czas serwera: {0}'.format(curr_time))
