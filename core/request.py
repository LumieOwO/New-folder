import ssl
import socket


class Request:
    def __init__(self,url):
        self.url = url
        parts = self.url.split('/')
        self.host = parts[2]
        self.path = '/' + '/'.join(parts[3:])
        self.headers = f"GET {self.path} HTTP/1.1\r\nHost: {self.host} \r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 \r\n\r\n"

    def get(self):
        if self.url.startswith("https://"):
            port = 443
            context = ssl.SSLContext()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssl_sock = context.wrap_socket(sock, server_hostname=self.host)
            try:
                ssl_sock.connect((self.host, 443))
            except:
                return -1,0
            ssl_sock.sendall(bytes(self.headers,"utf-8"))
            data = b""
            while True:
                recv_data = ssl_sock.recv(1024)
                if not recv_data:
                    break
                data += recv_data
            ssl_sock.close()
        else:
            port = 80
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((self.host, 80))
            except:
                return -1,0
            sock.sendall(bytes(self.headers,"utf-8"))
            data = b""
            while True:
                recv_data = sock.recv(1024)
                if not recv_data:
                    break
                data += recv_data
            sock.close()
        return data,port
