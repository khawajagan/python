#!/usr/bin/env python3
import turtle
import sys
import socket
import selectors
import types

mySelector = selectors.DefaultSelector()

def myConCircle():
    turtle.fillcolor('blue')
    turtle.pencolor('blue')
    turtle.forward(50)
    turtle.circle(20,steps=5)
    

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    myConCircle()
    print("==========\nAccepted connection from", addr,"\n==========")
    print("\U0001f600")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    mySelector.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print("==========\nClosing connection to", data.addr, "\n==========")
            mySelector.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print("\tEchoing", repr(data.outb), "to", data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
turtle.fillcolor('red')
turtle.pencolor('red')
turtle.begin_fill()
turtle.back(200)
turtle.circle(20)
print("Listening on", (host, port))
lsock.setblocking(False)
mySelector.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = mySelector.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    mySelector.close()