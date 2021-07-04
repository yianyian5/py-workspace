import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59'}
url1 = 'https://movie.douban.com/top250?start='
page = tuple(range(10))


def get_html(url, num):
    r = requests.get(url=url + str(num * 25) + '&filter=', headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return None


def get_content(html_1):
    soup = BeautifulSoup(html_1, 'lxml')
    return soup


df1 = pd.DataFrame(
    {
        "Index": [],
        "Name_of_Film": [],
        "Short_introduction": []
    }
)

for i in page:
    h = get_html(url1, i)
    if h is None:
        print('false')
        break
    else:
        s = get_content(h)
        title1 = s.find(class_="grid_view").find_all('li')
        for items in title1:
            if items.find(class_="inq") is None:
                df2 = pd.DataFrame(
                    {
                        "Index": [items.find(class_="").string],
                        "Name_of_Film": [items.find(class_="title").string],
                        "Short_introduction": ['']
                    }
                )
                df1 = pd.concat([df1, df2])
            else:
                df2 = pd.DataFrame(
                    {
                        "Index": [items.find(class_="").string],
                        "Name_of_Film": [items.find(class_="title").string],
                        "Short_introduction": [items.find(class_="inq").string]
                    }
                )
                df1 = pd.concat([df1, df2])

df1.to_excel("douban.xlsx", sheet_name="film", index=False)

