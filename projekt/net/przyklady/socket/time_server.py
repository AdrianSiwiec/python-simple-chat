import socket
import time

#utworzenie gniazda TCP, adres gniazda z rodziny IP4
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

#dowiązanie gniazda do portu 12345
s.bind(('', 12345)) 

#ustanowienie gniazda gniazdem oczekującym na zgłoszenia, z kolejką (nie obsłużonych przez accept()) zgłoszeń ograniczoną przez 5
s.listen(5)

while True:
	#odebranie polaczenia
	client,addr = s.accept() 
	print('Polaczenie z {0}'.format(addr))
	
	#konwersja stringu na bajty w kodowaniu UTF-8
	b = bytes(time.ctime(time.time()),'UTF-8')
	
	#wysłanie danych do klienta
	client.send(b) 
	
	#zamkniecie gniazda 	client.close()
	


