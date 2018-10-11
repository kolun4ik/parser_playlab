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
import os
import shutil
import sys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from lxml import html


class PlayLabParser:
    def __init__(self, BASE_URL='https://playlab.ru', path='e:\\',\
                    project='Catalog PlayLab', permit_save_img=False):
        self.BASE_URL = BASE_URL
        self.path = path
        self.project = project
        self.permit_save_img = permit_save_img
        self.page = ''
        self.catalog = []  # список категорий
        self.carts = []  # список карточек
        self.get_catalog(self.BASE_URL)

        if len(self.catalog) > 0:
            print("Заполняем каталог данными!")
            self.save_data(self.catalog)
        else:
            print('Не удалось сформировать каталог, либо каталог пуст!')
            sys.exit()

        if len(self.carts) > 0:
            print('Сохраняем карточки с товаром')
            self.save_carts(self.carts)
        else:
            print('Карточки сохранить не удалось!')

    def get_html(self, url):
        # получаем по url исходный код страницы на html
        user_agent = UserAgent()
        self.page = requests.get(url, headers={'user-agent': user_agent.chrome})
        if self.page.status_code == 200:
            return self.page.text
        else:
            return None

    def make_soup(self, url):
        # Завариваем супец
        html = self.get_html(url)
        if html:
            return BeautifulSoup(html, 'lxml')
        else:
            return None

    def get_catalog(self, url):
        # ищем на странице ul с классом "root" и проходим по всем элементам списка.
        # Помещаем данные в словарь. Формируем список словарей:
        # [{'name': name, 'url': url, 'image': img, 'category': category}]

        catalog_url = self.BASE_URL + '/toys/'
        soup = self.make_soup(catalog_url)
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

    def save_img(self, url, dir=''):
        image = requests.get('https://playlab.ru' + url)
        with open(dir+'/%s' % url.split('/')[-1], 'bw') as img:
            img.write(image.content)

    def save_data(self, catalog):
            # Определяем полный путь для каждой категории

            full_path = os.path.join(self.path, self.project)

            if os.path.exists(full_path) is False:
                os.mkdir(full_path)

            # Пробегаем по списку категорий
            for element in catalog:
                current_dir = os.path.join(full_path, element['name'])
                if os.path.exists(current_dir) is False:
                    os.makedirs(current_dir)

                # Парсим страницу с категорией товара, сохраняем все необходимые
                # данные в каталог со схожим именем.
                category_link = self.BASE_URL + element['url'] + '?SHOWALL_1=1'
                soup = self.make_soup(category_link)
                page_keywords = soup.find("meta", {"name": "keywords"})['content']
                page_desc = soup.find("meta", {"name": "description"})['content']
                page_title = soup.title.string
                page_text = soup.find('div', class_='section-description').get_text()

                file_info = current_dir + '\\' + element['name'] + '.txt'
                with open(file_info, 'w', encoding='utf8') as f_info:
                    data = {'title': page_title,
                            'description': page_desc,
                            'keywords': page_keywords,
                            'Описание': page_text,
                            }
                    for key, value in data.items():
                        f_info.write(f'{key}: {value}.\n')

                self.save_img(element['image'], current_dir)

                # Забираем ссылки на карточки товара с данной страницы
                items = soup.find('div', class_='items')\
                    .find('span', class_='desktop_wh').find_all('div', class_='item')
                for item in items:
                    cart_title = item.a.text
                    cart_url = item.a['href']
                    cart = {'title': cart_title.strip(),
                            'url': cart_url,
                            'category': element['name']}
                    self.carts.append(cart)

    def save_carts(self, carts):
        '''На входе получаем список карточек товаров. С каждой карточки товара забираем
        описание, ключевые слова, картинки и видео, и, сохряняем в соответсвующую директорию
        на диске ПК
        '''

        delete_symbol = {ord(s): '' for s in '\/:*"?<>|'}

        for cart in carts:
            cart_title = cart['title']
            cart_url = cart['url']
            cart_category = cart['category']
            cart_link = self.BASE_URL + cart_url + '?SHOWALL_1=1'
            soup = self.make_soup(cart_link)
            # В карточке товара нет атрибутов keywords и description, поэтому игнор
            # page_keywords = soup.find("meta", {"name":"keywords"})['content']
            # page_desc = soup.find("meta", {"name":"description"})['content']
            page_title = soup.title.string  # скорее всего потребуется сделать разбиение по "-"
            page_h1 = soup.h1.contents[0]
            cart_text = soup.article.find('div', class_='description')
            imgs_src = soup.article.find('div', class_='fotorama').find_all('img')
            full_path = os.path.join(self.path, self.project)
            current_dir = os.path.join(full_path, cart_category.translate(delete_symbol).strip(), cart_title.translate(delete_symbol).strip())
            if os.path.exists(current_dir) is False:
                    os.makedirs(current_dir)

            with open(current_dir + '/page_info.txt', 'w', encoding='utf8') as f:
                data = {'title': page_title,
                        'h1': page_h1,
                        'text': cart_text
                        }
                for key, value in data.items():
                        f.write(f'{key}: {value}.\n')

            if self.permit_save_img:

                for img in imgs_src:
                    img_path = img.get('src')
                    img_name = img_path.split('/')[-1]
                    img_src = requests.get(self.BASE_URL + img_path, stream=True)
                    print('Загружаю картинку', img_name)
                    try:
                        with open(current_dir + '/' + img_name, 'wb') as file:
                            shutil.copyfileobj(img_src.raw, file)
                    except Exception as e:
                        print(e)
                        print('Не удалось загрузить картинку: ', img_name)
                        print('Ссылка на картинку:', img_src)
        print('Процесс завершен!')


if __name__ == '__main__':

    app = PlayLabParser()
