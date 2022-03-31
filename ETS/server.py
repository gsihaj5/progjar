import socket
import logging


class Server:
    def __init__(self, ip, port):
        self.sock = None
        self.ip = ip
        self.port = port

    def create_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.bind((self.ip, self.port))
        print(f"starting up on {self.ip}:{self.port}")
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
        while True:
            server.accept_connection()
    except KeyboardInterrupt:
        logging.warning("Control-C: Program berhenti")
        exit(0)
    except Exception as ee:
        print("ERROR")
        print(ee)
        logging.info(f"ERROR: {str(ee)}")
    finally:
        server.close_socket()
