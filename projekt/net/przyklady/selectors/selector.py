import selectors
import socket

sel = selectors.DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    
    #ustawiamy kanał jako nieblokujący
    conn.setblocking(False)
    
    #rejestrujemy w selektorze, monitorujemy gotowość wykonania operacji READ, 
    # ostatni parametr to załącznik do klucza, który jest generowany podczas rejestracji
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 12345))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    #zwraca listę (key,events), gdzie events opisuje operacje IO gotowe do wykonania
    events = sel.select()
    print("OK - cos sie dzieje")
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
