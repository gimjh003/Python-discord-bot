import requests
from bs4 import BeautifulSoup

url = "http://www.quotationspage.com/random.php"

def quote_generator():
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    quotes = soup.find("dl")
    quote_main = quotes.find("dt").get_text()
    quote_author = quotes.find("dd").find("b").find("a").get_text()
    ret = f"\"{quote_main}\"\n\n{quote_author}"
    return ret