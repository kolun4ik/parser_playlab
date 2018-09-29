from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import pdb

def get_html(url):
        # получаем по url исходный код страницы на html
        user_agent = UserAgent()
        page = requests.get(url, headers={'user-agent': user_agent.chrome})
        if page.status_code == 200:
            return page.text
        else:
            return None

url = 'https://playlab.ru/toys/rubiks/?SHOWALL_1=1'
html = get_html(url)
soup = BeautifulSoup(html, 'lxml')

meta_keywords = soup.find("meta", {"name":"keywords"})['content']
meta_desc = soup.find("meta", {"name":"description"})['content']
title = soup.title.string
page_text = soup.find('div', class_='section-description').get_text()
items = soup.find('div', class_='items').find('span', class_='desktop_wh').find_all('div', class_='item')
for item in items:
    title_cart = item.a.text
    with open('carts.txt', 'a', encoding='utf8') as carts:
        carts.write(title_cart + '\n')
    # pdb.set_trace()
