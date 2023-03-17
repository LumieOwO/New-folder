from utils.httpsocket import HttpSocket, shutdown_http_socket
from gzip import decompress
import re

class Request:
    def __init__(self, url):
        self.url = url

    def get(self):
        if str(self.url).startswith("https://"):
            return self.requesting(port=443)
        else:
            return self.requesting(port=80)
        
    def requesting(self, port):
        sock = HttpSocket(url=self.url).create_http_socket(port=port)
        resp = b""
        while True:
            data = sock.recv(2048)
            if not data:
                break
            resp += data
        shutdown_http_socket(sock=sock)
        headers, content = resp.split(b"\r\n\r\n", 1)
        status_code = int(headers.split()[1])
        if status_code in [301, 302, 303, 307, 308]:
            new_location = ''
            for header in headers.split(b'\r\n'):
                if header.lower().startswith(b'location:'):
                    try:
                        new_location = header.split(b'location: ')[1]
                    except IndexError:
                        new_location = header.split(b'location: ')[0]
                    break
            self.url = new_location.decode()
            content, port = self.requesting(port)
        encoding = re.search(b"charset=(.*)", headers, re.IGNORECASE)
        if encoding:
            content = content.decode(encoding.group(1).decode(), errors="replace")
        elif headers.lower().count(b"content-encoding: gzip"):
            content = decompress(content).decode(errors="replace")
        else:
            content = content.decode(errors="replace")
        html_start = content.find("<!DOCTYPE html>")
        html_end = content.find("</html>") + 7
        content = content[html_start:html_end]
        print(content)
        return content, port
