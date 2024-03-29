import socket
import logging
import json
import os
import ssl
import threading

alldata = dict()
alldata['1'] = dict(nomor=1, nama="dean henderson", posisi="kiper")
alldata['2'] = dict(nomor=2, nama="luke shaw", posisi="bek kiri")
alldata['3'] = dict(nomor=3, nama="aaron wan-bissaka", posisi="bek kanan")
alldata['4'] = dict(nomor=4, nama="victor lindelof", posisi="bek tengah kanan")
alldata['5'] = dict(nomor=5, nama="pemain 5", posisi="pos 5")
alldata['6'] = dict(nomor=6, nama="pemain 6", posisi="pos 6")
alldata['7'] = dict(nomor=7, nama="pemain 7", posisi="pos 7")
alldata['8'] = dict(nomor=8, nama="pemain 8", posisi="pos 8")


def versi():
    return "versi 0.0.1"


def proses_request(request_string):
    # format request
    # NAMACOMMAND spasi PARAMETER
    cstring = request_string.split(" ")
    hasil = None
    try:
        command = cstring[0].strip()
        if (command == 'getdatapemain'):
            # getdata spasi parameter1
            # parameter1 harus berupa nomor pemain
            logging.warning("getdata")
            nomorpemain = cstring[1].strip()
            try:
                logging.warning(f"data {nomorpemain} ketemu")
                hasil = alldata[nomorpemain]
            except:
                hasil = None
        elif (command == 'versi'):
            hasil = versi()
    except:
        hasil = None
    return hasil


def serialisasi(a):
    # print(a)
    # serialized = str(dicttoxml.dicttoxml(a))
    serialized = json.dumps(a)
    logging.warning("serialized data")
    logging.warning(serialized)
    return serialized


def run_server(server_address, is_secure=False):
    # ------------------------------ SECURE SOCKET INITIALIZATION ----
    if is_secure:
        print(os.getcwd())
        cert_location = os.getcwd() + '/certs/'
        socket_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        socket_context.load_cert_chain(
            certfile=cert_location + 'domain.crt',
            keyfile=cert_location + 'domain.key'
        )
    # ---------------------------------

    # --- INISIALISATION ---
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    logging.warning(f"starting up on {server_address}")
    sock.bind(server_address)
    # Listen for incoming connections
    sock.listen(1000)

    while True:
        # Wait for a connection
        logging.warning("waiting for a connection")
        koneksi, client_address = sock.accept()
        logging.warning(f"Incoming connection from {client_address}")
        try:
            if is_secure:
                connection = socket_context.wrap_socket(
                    koneksi, server_side=True)
            else:
                connection = koneksi
            # Clean up the connection

            thread = threading.Thread(
                target=handle_request,
                args=(server_address, connection))

            thread.start()

        except ssl.SSLError as error_ssl:
            logging.warning(f"SSL error: {str(error_ssl)}")


def handle_request(server_address, connection):
    print("handling request")
    selesai = False
    data_received = ""  # string
    while True:
        data = connection.recv(32)
        print(f"received {data}")
        if data:
            data_received += data.decode()
            print(f"decoded data {data_received}")
            if "\r\n\r\n" in data_received:
                print("end of file")
                selesai = True

            if (selesai):
                hasil = proses_request(data_received)
                logging.warning(f"hasil proses: {hasil}")
                print(f"hasil proses: {hasil}")

                hasil = serialisasi(hasil)
                hasil += "\r\n\r\n"
                connection.sendall(hasil.encode())
                selesai = False
                data_received = ""  # string
                break

        else:
            break
    print("handling request done")


if __name__ == '__main__':
    secure = True

    if(secure):
        print("running ssl multi thread server")
    else:
        print("running no-ssl multi thread server")
    try:
        run_server(('0.0.0.0', 10000), is_secure=secure)
    except KeyboardInterrupt:
        logging.warning("Control-C: Program berhenti")
        exit(0)
    finally:
        logging.warning("seelsai")
