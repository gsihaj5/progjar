import socket
import logging
import threading


class Request:
    def __init__(self, ip, port, data):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = port
        self.data = data

    def connect(self):
        server_address = (self.ip, self.port)
        print(f"connecting to {server_address}")
        self.sock.connect(server_address)

    def send(self):
        self.connect()
        print(f"sending {self.data}")
        self.sock.sendall(self.data.encode())
        self.handle_response()

    def handle_response(self):
        amount_received = 0
        amount_expected = len(self.data)
        while amount_received < amount_expected:
            data = self.sock.recv(16)
            amount_received += len(self.data)
            print(f"{data}")
            logging.info(f"{data}")

    def send_with_thread(self):
        self.thread = threading.Thread(target=self.send, args=())
        self.thread.start()

    def join_thread(self):
        self.thread.join()


try:
    request1 = Request('172.16.16.101', 10000, "hello1111111111111111")
    request2 = Request('172.16.16.101', 10000, "222")
    request3 = Request('172.16.16.101', 10000,
                       "33333333333333333333333333333333")

    request1.send_with_thread()
    request2.send_with_thread()
    request3.send_with_thread()

    request1.join_thread()
    request2.join_thread()
    request3.join_thread()

    print("done")

except Exception as ee:
    logging.info(f"ERROR: {str(ee)}")
    exit(0)
finally:
    logging.info("closing")
