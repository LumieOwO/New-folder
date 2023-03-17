import socket
import ssl

context = ssl.create_default_context()
def shutdown_http_socket(sock):
        if sock is not None:
            try:
                sock.shutdown(2)
            except OSError:
                pass
            sock.close()
class HttpSocket:
    def __init__(self, url):
        self.url = url
        try:
            parts = self.url.split('/')
        except:
            parts = self.url.split(b'/')
        self.host = parts[2]
        try:
            self.path = '/' + '/'.join(parts[3:])
        except:
            self.path = b'/' + b'/'.join(parts[3:])
        self.headers = f"GET {self.path} HTTP/1.1\r\nHost: {self.host} \r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 \r\n\r\n"

    def create_http_socket(self, port=80):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if port == 443:
            try:
                sock = context.wrap_socket(sock=sock, server_side=False, suppress_ragged_eofs=False, do_handshake_on_connect=True, server_hostname=self.host)
                #sock.do_handshake()
            except ssl.SSLError as e:
                print(f"SSL error: {e}")
                return None
            except socket.gaierror as e:
                print(f"DNS resolution error: {e}")
                return None
        try:
            sock.connect((self.host, port))
            sock.sendall(bytes(self.headers, "utf-8"))
        except Exception as e:
            print(f"Socket error: {e}")
            return None
        return sock
