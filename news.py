import requests
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}
url_politics = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"
url_economy = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"
url_society = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102"
url_life_culture = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103"
url_IT_science = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105"
url_world = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104"

def news_headline(url):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    headline = soup.find("a", {"class":"cluster_text_headline"}).get_text()
    link = soup.find("a", {"class":"cluster_text_headline"})["href"]
    return headline, link

def news_get_politics():
    headline, link = news_headline(url_politics)
    return headline, link

def news_get_economy():
    headline, link = news_headline(url_economy)
    return headline, link

def news_get_society():
    headline, link = news_headline(url_society)
    return headline, link

def news_get_life_culture():
    headline, link = news_headline(url_life_culture)
    return headline, link

def news_get_IT_science():
    headline, link = news_headline(url_IT_science)
    return headline, link

def news_get_world():
    headline, link = news_headline(url_world)
    return headline, link