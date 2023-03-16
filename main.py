from core.arguments import parse_args
from core.worker import Worker
from core.request import Request
from core.htmlparser import HtmlParser
if __name__ == '__main__':
    args = parse_args()
    threads:int = args.threads
    url:str = args.url
    html_code,port = Request(url=url).get()
    urls:list = HtmlParser(html_code=html_code,int_port=port).parse()
    for i in range(threads):
        try:
            Worker(args=args).controller(urls=urls[i])
        except IndexError:
            pass