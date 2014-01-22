#!/usr/bin/env python
import random
import socket
import time

def handle_get(conn, path):
    if path == '/':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html><body>')
        conn.send('<h1>Hello, world.</h1>')
        conn.send("This is rutowsk1's Web server.<br>")
        conn.send("<a href='/content'>Content</a><br>")
        conn.send("<a href='/file'>Files</a><br>")
        conn.send("<a href='/image'>Images</a>")
        conn.send('</html></body>')
    elif path == '/content':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html><body>')
        conn.send('<h1>Content Page</h1>')
        conn.send('Stuff about things')
        conn.send('</html></body>')
    elif path == '/file':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html><body>')
        conn.send('<h1>File Page</h1>')
        conn.send('Files')
        conn.send('</html></body>')
    elif path == '/image':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html><body>')
        conn.send('<h1>Image Page</h1>')
        conn.send('Images')
        conn.send('</html></body>')
    else:
        conn.send('HTTP/1.0 404 Not Found\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<html><body>')
        conn.send('<h1>404</h1>')
        conn.send('This page does not exist')
        conn.send('</html></body>')

def handle_post(conn):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('Hello World')
    conn.send('</html></body>')

def handle_connection(conn):
    req = conn.recv(1000)
    req = req.split('\r\n')[0].split(' ')
    reqType = req[0]
    path = req[1]
    if reqType == 'GET':
        handle_get(conn, path)
    elif reqType == 'POST':
        handle_post(conn)
    conn.close()

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)
        

if __name__ == "__main__":
    main()

