# Парсер сайта https://playlab.ru
# Исдодные данные:
# - сайт https://playlab.ru
# - выгрузка каталога в файл Exel: артикул, бренд, название, ориентировочная цена, описание, ссылка на фото, ссылка на товар.
# Задание.
# 1. В папке назаначения создать структуру, повторяющую исходный каталог сайта исходника.
# 2. В разделы вывести описание категории, картинку категории.
# 3. Сохранить в отдельном файле значения поля keywords и description
# 4. Используя данные приложенного файла: сформировать карточки товара, скачать все картинки, прилагаемые к товару и разместить все по соответсвующим категориям каталога.
# 5. Вести логирование совершенных действий для последующего анализа.

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests


class PlayLabParser:
    def __init__(self, url='https://playlab.ru/toys/', path='', project='Catalog'):
        self.url = url
        self.path = path
        self.project = project
        self.page = ''
        print(self.get_html(self.url))


    def get_html(self, url):
        # получаем по url исходный код страницы на html
        user_agent = UserAgent()
        self.page = requests.get(self.url, headers={'user-agent': user_agent.chrome})
        return self.page.text



if __name__ == '__main__':
    app = PlayLabParser()


# Подсказка:
# products = {}   # product name - key product link - value
# product_names = [div.div.a.span.string for div in soup.find_all('div',class_='')]
# product_links = [div.div.a['href'] for div in soup.find_all('div',class_='')]
# products = {div.div.a.span.string:div.div.a['href'] for div in soup.find_all('div',class_='')}
# for key,value in products.items():
#     print(key , '   -->',value)