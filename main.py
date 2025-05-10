from with_api import crawl
from with_ollama import client

def main():
    crawler = crawl.Crawler()
    crawler.start()
    crawler.foryou()


if __name__ == "__main__":
    main()