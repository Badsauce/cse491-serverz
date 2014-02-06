#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi

from mimetools import Message
from StringIO import StringIO

def handle_submit(conn,url):
    query = urlparse.parse_qs(url.query)
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send("Hello Mr. ")
    conn.send(query['firstname'][0])
    conn.send(" ")
    conn.send(query['lastname'][0])
    conn.send('.')
    conn.send('</html></body>')

def handle_form(conn,url):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send("<form action='/submit' method='POST'")
    conn.send('enctype="multipart/form-data"')
    conn.send(">")
    conn.send("First name:")
    conn.send("<input type='text' name='firstname'>")
    conn.send("Last name:")
    conn.send("<input type='text' name='lastname'>")
    conn.send("<input type='submit'>")
    conn.send("</form>")
    conn.send('</html></body>')

def handle_root(conn, url):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('<h1>Hello, world.</h1>')
    conn.send("This is rutowsk1's Web server.<br>")
    conn.send("<a href='/content'>Content</a><br>")
    conn.send("<a href='/file'>Files</a><br>")
    conn.send("<a href='/image'>Images</a>")
    conn.send('</html></body>')

def handle_content(conn, url):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('<h1>Content Page</h1>')
    conn.send('Stuff about things')
    conn.send('</html></body>')

def handle_file(conn, url):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('<h1>File Page</h1>')
    conn.send('Files')
    conn.send('</html></body>')

def handle_image(conn, url):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('<h1>Image Page</h1>')
    conn.send('Images')
    conn.send('</html></body>')

def handle_404(conn, url):
    conn.send('HTTP/1.0 404 Not Found\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send('<h1>404</h1>')
    conn.send('This page does not exist')
    conn.send('</html></body>')

def handle_get(conn, url):
    path = url.path
    if path == '/':
        handle_root(conn,url)
    elif path == '/form':
        handle_form(conn,url)
    elif path == '/submit':
        handle_submit(conn,url)
    elif path == '/content':
        handle_content(conn, url)
    elif path == '/file':
        handle_file(conn, url)
    elif path == '/image':
        handle_image(conn, url)
    else:
        handle_404(conn, url)

def handle_post(conn,content):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<html><body>')
    conn.send("Hello Mr. ")
    conn.send(content['firstname'])
    conn.send(" ")
    conn.send(content['lastname'])
    conn.send('.')
    conn.send('</html></body>')

def read_head(conn):
    message = ''
    while '\r\n\r\n' not in message:
        message += conn.recv(1)
    return message.rstrip()

def handle_connection(conn):
    rawHead = read_head(conn)
    headList = rawHead.split('\r\n')
    contentType = [s for s in headList if 'Content-Type' in s]
    req = headList[0].split(' ')
    reqType = req[0]
    if reqType == 'GET':
        path = req[1]
        url = urlparse.urlparse(path)
        handle_get(conn, url)
    elif reqType == 'POST':
        requestLine, raw_headers = rawHead.split('\r\n',1)
        headers = raw_headers.split('\r\n')

        headDict = {}
        for line in headers:
            k, v = line.split(': ', 1)
            headDict[k.lower()] = v

        content = conn.recv(int(headDict['content-length']))
        contentType = headDict['content-type']

        if contentType == 'application/x-www-form-urlencoded':
            content = urlparse.parse_qs(content)
            content['firstname'] = content['firstname'][0]
            content['lastname'] = content['lastname'][0]
        elif 'multipart/form-data' in contentType:
            environ = {}
            environ['REQUEST_METHOD'] = 'POST'

            form = cgi.FieldStorage(headers=headDict, fp=StringIO(content), environ=environ)

            content = {}
            content['firstname'] = form['firstname'].value
            content['lastname'] = form['lastname'].value
        handle_post(conn,content)
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

