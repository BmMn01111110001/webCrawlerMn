# -*- coding: utf-8 -*-
"""news.mn_crawler.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U3MAXpMbHJF2jdCv_M2MI3jIHK9Dl6j5
author : Enkhmanlai Bayarmagnai
# Web Crawlers: News.mn
"""

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time


"""### Нэг функц болгох хугацааг хэмжих

Энэ скрипт нь мэдээ авахад хэр их цаг хугацаа шаардагдахыг сонирхож байна. Үүний тулд бид бүгдийг нэг функц болгон байрлуулаад дараа нь дуудна.
"""

def news_crawler(url):
    # url тодорхойлох
    
    c = url[24:]
    y = c.replace('shar-medee/', 'шар мэдээ')
    y = y.replace('entertainment/', 'энтертаймент')
    y = y.replace('sport/', 'спорт')
    y = y.replace('ediin-zasag/','эдийн засаг')
    y = y.replace('uls-tur/', 'улс төр')
    y = y.replace('niigem/', 'нийгэм')
    y = y.replace('delhii/', 'дэлхий')

    # Хүсэлт
    r1 = requests.get(url)
    r1.status_code

    # Нүүр хуудасны агуулгыг хадгалах болно
    coverpage = r1.content

    # Soup үүсгэх
    soup1 = BeautifulSoup(coverpage, 'html5lib')

    # Мэдээ таних
    coverpage_news = soup1.find_all('h1', class_='entry-title')
    len(coverpage_news)
    
    number_of_articles = 5

    # Контент, холбоос, гарчигийн хоосон жагсаалт
    news_contents = []
    list_links = []
    list_titles = []

    for n in np.arange(0, number_of_articles):

        # Нийтлэл биш тул "live" хуудсыг орхих хэрэгтэй
        if "live" in coverpage_news[n].find('a')['href']:  
            continue

        # Нийтлэлийн холбоосыг авч байна
        link = coverpage_news[n].find('a')['href']
        list_links.append(link)

        # Гарчиг авч байна
        title = coverpage_news[n].find('a').get_text()
        list_titles.append(title)

        # Агуулга унших (энэ нь догол мөрүүдээр хуваагдана)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html5lib')
        body = soup_article.find_all('div', class_='has-content-area')
        x = body[0].find_all('p')

        # Догол мөрүүдийг нэгтгэх
        list_paragraphs = []
        for p in np.arange(0, len(x)):
            paragraph = x[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)

        news_contents.append(final_article)

    # df_features
    df_features = pd.DataFrame(
         {'Мэдээлэл': news_contents,
          'Ангилал': y
        })

    # df_show_info
    df_show_info = pd.DataFrame(
        {'Мэдээний гарчиг': list_titles,
         'Мэдээний линк': list_links,
         'Мэдээллийн сайт': 'News.mn'})

    
    return df_features
# url оруулна
url = "https://news.mn/angilal/ediin-zasag/"
df  = news_crawler(url)
data = df.to_csv(r'news.csv', index = False)

