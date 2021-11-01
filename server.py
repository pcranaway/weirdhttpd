import socket
import weirdhttp as http

DEFAULT_PAGE = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Hello, World!</title>
    </head>
    <body>
        <h1>Hello, World!</h1>
    </body>
'''

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []

    def accept(self, sock):
        client, address = sock.accept()
        self.clients.append(client)
        print(f'Client {address} connected')

        while True:
            data = client.recv(1024)
            if not data:
                break

            request = http.Request.parse(data.decode())
            print(request.encode())

            response = http.Response(200, {
                'Content-Type': 'text/html',
                'Content-Length': len(DEFAULT_PAGE),
                'Connection': 'close'
            }, DEFAULT_PAGE)

            client.send(response.encode().encode())

    def bind(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:

            sock.bind((self.host, self.port))
            sock.listen(5)

            while True:
                self.accept(sock)

        except Exception:

            sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            exit(0)
