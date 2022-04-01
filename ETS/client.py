import socket
import logging
import threading
import ssl
import os
import random


class Request:
    def __init__(self, ip, port, data, secure=False):
        self.ip = ip
        self.port = port
        self.data = data
        self.secure = secure

    def make_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.ip, self.port)
        logging.warning(f"connecting to {server_address}")
        self.sock.connect(server_address)

    def make_secure_socket(self):
        try:
            # get it from https://curl.se/docs/caextract.html
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.verify_mode = ssl.CERT_OPTIONAL
            context.load_verify_locations(os.getcwd() + '/domain.crt')

            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (self.ip, self.port)
            logging.warning(f"connecting to {server_address}")
            self.sock.connect(server_address)
            secure_socket = context.wrap_socket(
                self.sock, server_hostname=self.ip)
            logging.warning(secure_socket.getpeercert())
            self.sock = secure_socket

        except Exception as ee:
            logging.warning(f"error {str(ee)}")

    def send(self):
        if(self.secure):
            self.make_secure_socket()
        else:
            self.make_socket()
        print(f"sending {self.data}")
        self.sock.sendall(self.data.encode())
        self.handle_response()

    def handle_response(self):
        amount_received = 0
        amount_expected = len(self.data)
        while amount_received < amount_expected:
            data = self.sock.recv(16)
            amount_received += len(self.data)
            print(f"response : {data}")
            logging.info(f"{data}")

    def send_with_thread(self):
        self.thread = threading.Thread(target=self.send, args=())
        self.thread.start()

    def join_thread(self):
        self.thread.join()


def send_random_request():
    id_pemain = random.randint(1, 10)
    request = Request(
        ip='172.16.16.101',
        port=10000,
        data=f"getdatapemain {id_pemain}\r\n\r\n"
    )
    request.send()


try:
    send_random_request()
    send_random_request()
    send_random_request()

    print("done")

except Exception as ee:
    logging.info(f"ERROR: {str(ee)}")
    exit(0)
finally:
    logging.info("closing")
