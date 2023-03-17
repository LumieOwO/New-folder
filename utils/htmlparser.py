import re

class HtmlParser:
    def __init__(self, html_code: bytes, int_port: str):
        try:
            self.html_code: str = html_code.lower()
        except:
            self.html_code = html_code.decode().lower()
        self.hrefs: list = []
        self.str_port: str = int_port

    def parse(self) -> list:
        port: str = "http:"
        if self.str_port == 443:
            port: str = "https:"
        regex = r'<a\s+[^>]*href="([^"]*)"'
        matches = re.findall(regex, self.html_code)
        for match in matches:
            if match.startswith("http"):
                self.hrefs.append(f"{match}")
            else:
                self.hrefs.append(f"{port}{match}")
        return self.hrefs