# Сохраняем всю инфломацию по карточке товара
import requests
import shutil
import pdb
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def get_html(url):
        # получаем по url исходный код страницы на html
        user_agent = UserAgent()
        page = requests.get(url, headers={'user-agent': user_agent.chrome})
        if page.status_code == 200:
            return page.text
        else:
            return None


url = 'https://playlab.ru/toys/mirror-cubes/mirror-cube-fisher-silver/?SHOWALL_1=1'
html = get_html(url)
soup = BeautifulSoup(html, 'lxml')

title = soup.title.string
page_h1 = soup.h1.contents[0]
cart_text = soup.article.find('div', class_='description')
imgs_src = soup.article.find('div', class_='fotorama').find_all('img')
for img in imgs_src:
    img_path = img.get('src')
    img_name = img_path.split('/')[-1]
    img_src = requests.get('https://playlab.ru' + img_path, stream=True)
    print('Загружаю картинку', img_name)
    
    try:
        with open(img_name, 'wb') as file:
            shutil.copyfileobj(img_src.raw, file)
    except Exception as e:
        print(e)
        print('Не удалось загрузить картинку с именем: ', img_name)
        print('Ссылка на картинку:', img_src)
