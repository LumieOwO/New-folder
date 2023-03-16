from core.request import Request
from core.htmlparser import HtmlParser


class Worker:
    def __init__(self,args) -> None:
            self.threads:int = args.threads
            self.origin:str = args.url
            self.urlss = []

    def fix_url(self,url):
        if url.startswith("https://"):
            return url
        elif url.startswith("https:/"):
            return url.replace("https:/", "https://")

    def url_validator(self, url):
        for i in range(len(url)):
             if url[i] == "/" and url[i-1] == ":" and url[i+1] == "/":
                  return True
             else:
                  return False
    
    def controller(self,urls:str):
            try:
                html_code, port = Request(url=urls).get()
                urlst: list = HtmlParser(html_code=html_code, int_port=port).parse()
                self.urlss.extend(urlst)
                for url in self.urlss:
                    if not self.url_validator(url):
                        continue
                    html_code, port = Request(url=url).get()
                    if html_code == -1:
                        self.__writetxt()
                    urlst: list = HtmlParser(html_code=html_code, int_port=port).parse()
                    self.urlss.extend(urlst)
                self.__writetxt()
            except:
                 self.__writetxt()
    def __writetxt(self):
        with open("urls.txt","w") as f:
            for i in self.urlss:
                f.write(i)
                f.write("\n")
            f.close()
        exit(0)
                
