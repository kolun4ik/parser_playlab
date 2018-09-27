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


class PlayLabParser:
    def __init__(self, url='https://playlab.ru', path='e:\\', project='Catalog PlayLab'):
        self.url = url
        self.path = path
        self.project = project
        self.page = ''
        self.catalog = []
        self.get_catalog(self.url)
        self.save_data(self.catalog)


    def get_html(self, url):
        # получаем по url исходный код страницы на html
        user_agent = UserAgent()
        self.page = requests.get(url, headers={'user-agent': user_agent.chrome})
        if self.page.status_code == 200:
            return self.page.text
        else:
            return None


    def get_catalog(self, url):
        # ищем на странице ul с классом "root" и проходим по всем элементам списка.
        # Помещаем данные в словарь. Формируем список словарей:
        # [{'name': name, 'url': url, 'image': img, 'category': category}]
        catalog_url = self.url + '/toys/'
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

    
    def save_img(self, url, dir=''):
        image = requests.get('https://playlab.ru' + url)
        with open(dir+'/%s' % url.split('/')[-1], 'bw') as img:
            img.write(image.content)


    def save_data(self, catalog):
        if len(catalog) == 0:
            print("Каталог пустой!")
            quit()
        else:
            print("Заполняем каталог данными!")
            # Определяем полный путь для каждой категории
            full_path = os.path.join(self.path, self.project)
            if os.path.exists(full_path) is False:
                os.mkdir(full_path)
            # Пробегаем по списку категорий
            for element in catalog:
                current_dir = os.path.join(full_path, element['name'])
                if os.path.exists(current_dir) is False:
                    os.makedirs(current_dir)
                self.save_img(element['image'], current_dir)

                source = str(self.url + element['url'])
                soup = BeautifulSoup(self.get_html(source), 'lxml')
                page_keywords = soup.find("meta", {"name":"keywords"})['content']
                page_desc = soup.find("meta", {"name":"description"})['content']
                page_title = soup.title.string
                page_text = soup.find('div', class_='section-description').get_text()
                pdb.set_trace()

                with open(current_dir + '/page_info.txt', 'w', encoding='utf8') as f_info:
                    data = {'title': page_title,
                            'description': page_desc,
                            'keywords': page_keywords,
                            'Описание': page_text,
                            }
                    for key, value in data.items():
                        f_info.write(f'{key}: {value}.\n')
                quit()






if __name__ == '__main__':
    app = PlayLabParser()


# Подсказка:
# products = {}   # product name - key product link - value
# product_names = [div.div.a.span.string for div in soup.find_all('div',class_='')]
# product_links = [div.div.a['href'] for div in soup.find_all('div',class_='')]
# products = {div.div.a.span.string:div.div.a['href'] for div in soup.find_all('div',class_='')}
# for key,value in products.items():
#     print(key , '   -->',value)