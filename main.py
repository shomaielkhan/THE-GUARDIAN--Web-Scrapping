from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime
import time

chrome_options= Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")


s= Service("C:/Users/User-PC/Desktop/Selenium/chromedriver-win64/chromedriver-win64/chromedriver.exe")
driver=webdriver.Chrome(service=s, options=chrome_options)

news=[]
author=[]
date=[]

url="https://www.theguardian.com/"
driver.get(url)

WebDriverWait(driver, 10).until(
    ec.presence_of_all_elements_located((By.XPATH, "/html/body/main/div[1]/section/div[3]/ul[1]/li[1]/div/div/a"))
)

soup= BeautifulSoup(driver.page_source, "html.parser")
#print(soup.prettify()[:5000])  # First 2000 characters

#print(soup)


articles= soup.find_all("div", class_="dcr-f9aim1")

for article in articles[:10]:
    article_link=article.find("a", class_="dcr-2yd10d")

    link=article_link['href']
    title=article.get_text(strip=True)

    author_tag = article.select_one("a.auto tag link") or article.find("a",rel="author")
    author_name = author_tag.text.strip() if author_tag else "Unknown"

    time_tag=article.find("time")
    if time_tag and time_tag.has_attr("datetime" ):
        published_time= datetime.fromisoformat(time_tag["datetime"].replace("Z", "")).strftime('%I:%M %p')
    else:
        published_time="Unknown"
        
    if article_link:
        news.append({'Time':published_time,'Article title':title, 'Author': author_name, 'Link':link})

base_url="https://www.theguardian.com/"

for items in news:
    items['Link']= base_url + items['Link']

df=pd.DataFrame(news)   
#print(df)
df.to_csv("Article links 2.csv")
driver.quit()