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

import requests
import pdb
import os
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from lxml import html
from pprint import pprint


class PlayLabParser:
    def __init__(self, url='https://playlab.ru/toys/', path='', project='Catalog PlayLab'):
        self.url = url
        self.path = path
        self.project = project
        self.page = ''
        self.catalog = []
        self.get_catalog(self.url)


    def get_html(self, url):
        # получаем по url исходный код страницы на html
        user_agent = UserAgent()
        self.page = requests.get(self.url, headers={'user-agent': user_agent.chrome})
        if self.page.status_code == 200:
            return self.page.text
        else:
            return None


    def get_catalog(self, url):
        # ищем на странице ul с классом "root" и проходим по всем элементам списка.
        # Помещаем данные в словарь. Формируем список словарей:
        # [{'name': name, 'url': url, 'image': img, 'categiry': category}]
        
        page_code = self.get_html(url)

        if page_code is not None:
            soup = BeautifulSoup(page_code, 'lxml')
            data = soup.find('ul', class_='root').li.ul.contents
        
            for punkt in data:
                if punkt == ' ':
                    continue

                element = html.fromstring(str(punkt))
                elements_name = element.xpath('//a/text()')[0]
                elements_url = element.xpath('//a/@href')[0]
                elements_image = element.xpath('//img/@src')[0]
                self.catalog.append({'name': elements_name,
                                     'url': elements_url,
                                     'image': elements_image,
                                     'category': '/'})




if __name__ == '__main__':
    app = PlayLabParser()


# Подсказка:
# products = {}   # product name - key product link - value
# product_names = [div.div.a.span.string for div in soup.find_all('div',class_='')]
# product_links = [div.div.a['href'] for div in soup.find_all('div',class_='')]
# products = {div.div.a.span.string:div.div.a['href'] for div in soup.find_all('div',class_='')}
# for key,value in products.items():
#     print(key , '   -->',value)