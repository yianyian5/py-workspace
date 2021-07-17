import pandas as pd
from selenium import webdriver
import time
from bs4 import BeautifulSoup

from selenium.webdriver import ActionChains

driverfile_path = r'D:\python workspace\edgedriver_win32\msedgedriver.exe'
driver1 = webdriver.Edge(executable_path=driverfile_path, capabilities={"browserName": "MicrosoftEdge",
                                                                        "version": "",
                                                                        "platform": "WINDOWS",
                                                                        "ms:edgeOptions": {
                                                                            'extensions': [],
                                                                            'args': ['--headless',
                                                                                     '--disable-gpu']}})
driver1.get("http://www.bilibili.com")

element3 = driver1.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/form/input")
element3.send_keys("焦安溥")
time.sleep(2)
button1 = driver1.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div/form/div/button")
button1.click()
time.sleep(5)
search_window = driver1.window_handles
driver1.switch_to.window(search_window[1])


def switch_pages():
    next_page = driver1.find_element_by_css_selector("#all-list > div.flow-loader > div.page-wrap > div > ul > "
                                                     "li.page-item.next > button")
    next_page.click()
    time.sleep(2)


df1 = pd.DataFrame(
    {
        "Name_of_Video": [],
        "publisher": [],
        "data": [],
        "views": []
    }
)

for ii in range(1, 20):
    s = BeautifulSoup(driver1.page_source, "lxml")
    title1 = s.find(class_="video-list clearfix").find_all('li')
    for items in title1:
        df2 = pd.DataFrame(
            {
                "Name_of_Video": [items.find("a")['title']],
                "publisher": [items.find(class_="so-icon").get_text(strip=True)],
                "data": [items.find(class_="so-icon time").get_text(strip=True)],
                "views": [items.find(class_="so-icon watch-num").get_text(strip=True)]
            }
        )
        df1 = pd.concat([df1, df2])
    switch_pages()
df1.to_excel("bilibili.xlsx", sheet_name="video", index=False)
