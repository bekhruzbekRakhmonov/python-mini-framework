import socket

DATA_PAYLOAD = 1024 * 8

class TCPServer:
    def __init__(self, host='127.0.0.1', port=8000):
        self.__host = host
        self.__port = port
        self.__is_listening = False
        self.__is_runnning = False

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(sock)
        self.sock = self.set_options(sock)


    def set_options(self,sock):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # sock.setblocking(False)

        return sock

    def bind(self,sock):
        sock.bind((self.__host, self.__port))

    def run(self):
        """Starts TCP server"""

        # try:
        self.sock.listen()
        self.log_info(f"Server is listening at http://{self.__host}:{self.__port}")
        while True:
            conn, addr = self.sock.accept()
            self.log_info("Connected by", addr)
            data = conn.recv(DATA_PAYLOAD) 

            response = self.handle_request(data)

            conn.sendall(response)
            conn.close()

        # except Exception as e:
        #     self.log_error(e)

    def handle_request(self, data):
        """
        Handles incoming data and returns a response.
        Override this in subclass.
        """
        return data

    def close(self):
        """Close the connections"""

        if self.sock is None:
            return 

        try:
            self.sock.close()
        except socket.error as e:
            self.log_error("Failed to close connection",e)

        self.sock = None


    def log_error(self,*args):
        print("[ERROR]",*args)
    
    def log_info(self,*args):
        print("[INFO]",*args)