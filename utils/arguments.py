import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", "--threads",
        default=11,
        type=int,
        help="Number of threads ",
        metavar="<int>")    
    parser.add_argument(
        "-url",
        type=str,
        help="url to start crawling from",
        metavar="<str>",
        required=True
    )
    args = parser.parse_args()
    return args
