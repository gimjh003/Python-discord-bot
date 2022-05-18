import requests
from bs4 import BeautifulSoup

def get_daily_eng_words():
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%98%A4%EB%8A%98%EC%9D%98+%EC%98%81%EB%8B%A8%EC%96%B4"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    daily_eng_words_html = soup.find("ul", attrs={"class":"_sap_list"})
    daily_eng_word_en = daily_eng_words_html.find_all("li", attrs={"class":"_sap_item"})
    daily_eng_words = {}
    for word in daily_eng_word_en:
        word_spell = word.find("a").get_text()
        word_mean = word.find("span", {"class":"mean"}).get_text()
        daily_eng_words[word_spell] = word_mean
    return daily_eng_words

def format_words(words):
    return_str = ""
    for word in words:
        return_str += f"{word} : {words[word]}\n"
    return return_str