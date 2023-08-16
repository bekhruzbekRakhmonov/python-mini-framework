import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_default_certs()

DATA_PAYLOAD = 2048

class UDPServer:
    def __init__(self, host="127.0.0.1", port=9000):
        self.host = host
        self.port = port

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
        sock.bind((self.host,self.port))
        # sock.listen()

        while True:
            # conn, addr = sock.accept()
            # print(f"connected by {addr}")
            data, address = sock.recvfrom(DATA_PAYLOAD)
            print("received %s bytes from %s" % (len(data), address))
            print("Data: %s" %data)
            if data:
                sent = sock.sendto(data, address)
                print("sent %s bytes back to %s" % (sent, address))

s = UDPServer()
s.start()