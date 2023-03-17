from utils.arguments import parse_args
from core.worker import Worker
from core.request import Request
from utils.htmlparser import HtmlParser
import multiprocessing
import time
if __name__ == '__main__':
    multiprocessing.freeze_support()
    args = parse_args()
    threads:int = args.threads
    url:str = args.url
    html_code,port = Request(url=url).get()
    urls:list = HtmlParser(html_code=html_code,int_port=port).parse()
    print(urls)
    for i in range(threads):
        try:
            Worker(args=args).controller(urls=urls[i])
        except IndexError:
            break