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
import pdb


class PlayLabParser:
    def __init__(self, url='https://playlab.ru/toys/', path='', project='Catalog'):
        self.url = url
        self.path = path
        self.project = project
        self.page = ''
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
        # ищем на странице ul с классом "root" и проходим по всем элементам списка:
        # <ul class="root">
        #     <li>
        #         <a href="#">name</a>
        #         <div class="cat_pic"><img src="#" alt=""></div>
        #     </li>
        #     <li class="parent">
        #         <a href="#">name</a>
        #         <div class="cat_pic"><img src="#" alt=""></div>
        #         <ul>
        #             <li>
        #                 <a href="#">name</a>
        #                 <div class="cat_pic"><img src="" alt=""></div>
        #             </li>
        #         </ul>
        #     </li>
        # </ul>
        # Помещаем данные в словарь. Формируем список словарей:
        # [{'name': name, 'url': url, 'image': img, 'categiry': category}]
        # Подсказка: http://wiki.python.su/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%86%D0%B8%D0%B8/BeautifulSoup
        html = self.get_html(url)
        if html is not None:
            # pdb.set_trace()
            soup = BeautifulSoup(html, 'lxml')
            data = soup.find('ul', class_='root').li.ul.descendants

            for  punkt in data:
                print(punkt)
                print('*'*50)



if __name__ == '__main__':
    app = PlayLabParser()


# Подсказка:
# products = {}   # product name - key product link - value
# product_names = [div.div.a.span.string for div in soup.find_all('div',class_='')]
# product_links = [div.div.a['href'] for div in soup.find_all('div',class_='')]
# products = {div.div.a.span.string:div.div.a['href'] for div in soup.find_all('div',class_='')}
# for key,value in products.items():
#     print(key , '   -->',value)
