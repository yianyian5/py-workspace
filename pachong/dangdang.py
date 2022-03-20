import pandas as pd
import requests
from bs4 import BeautifulSoup

url2 = "http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-all-0-0-1-"
page = list(range(1, 26))
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59'}


def get_html(url, num):
    r = requests.get(url=url + str(num), headers=headers)
    if r.status_code == 200:
        return r.text
    else:
        return None


def get_content(html_1):
    soup = BeautifulSoup(html_1, 'lxml')
    return soup


r1 = requests.get(url=url2 + str(1), headers=headers)
soup1 = BeautifulSoup(r1.text, 'lxml')

df1 = pd.DataFrame(
    {
        "Index": [],
        "Name_of_Book": [],
        "publisher": [],
        "star": []
    }
)

for i in page:
    h = get_html(url2, i)
    if h is None:
        print('false')
        break
    else:
        s = get_content(h)
        title2 = s.find(class_="bang_list clearfix bang_list_mode").find_all('li')
        for items in title2:
            if items.find(class_="list_num red") is None:
                df2 = pd.DataFrame(
                    {
                        "Index": [items.find(class_="list_num").string],
                        "Name_of_Book": [items.find(class_="name").find("a")['title']],
                        "publisher": [items.find_all(class_="publisher_info")[1].find("a").string],
                        "star": [items.find(class_="star").find("a").string]
                    }
                )
                df1 = pd.concat([df1, df2])
            else:
                df2 = pd.DataFrame(
                    {
                        "Index": [items.find(class_="list_num red").string],
                        "Name_of_Book": [items.find(class_="name").find("a")['title']],
                        "publisher": [items.find_all(class_="publisher_info")[1].find("a").string],
                        "star": [items.find(class_="star").find("a").string]
                    }
                )
                df1 = pd.concat([df1, df2])


df1.to_excel("dangdang.xlsx", sheet_name="book", index=False)
