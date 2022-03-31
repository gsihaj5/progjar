import socket
import logging


class Server:
    def __init__(self, ip, port):
        self.sock = None

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)

        self.sock.bind(self.ip, self.port)
        logging.info(f"starting up on {self.ip}:{self.port}")
        self.sock.listen(1)

    def close_socket(self):
        self.sock.close()

    def accept_connection(self):
        connection, client_address = self.sock.accept()
        self.receive_data(connection)
        connection.close()

    def receive_data(self, connection):
        while True:
            data = connection.recv(32)
            logging.info(f"received {data}")
            if data:
                logging.info("sending back data")
                connection.sendall(data)
            else:
                # no more data inside connection
                break


if __name__ == '__main__':
    server = Server(ip='0.0.0.0', port=10000)
    try:
        server.create_socket()
    except Exception as e:
        logging.log(f"ERROR: {str(e)}")
    finally:
        server.close_socket()

    while True:
        server.accept_connection()
