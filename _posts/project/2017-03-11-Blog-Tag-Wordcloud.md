---
layout: post
title: 使用 wordcloud 制作 博客标签云
category: project
description: 根据 标题 或者 博客内容 各测试了一下，都是 Python 词频最高。。。
---

前几天学习了一下 [wordcloud](http://amueller.github.io/word_cloud/) 词云，是一个用文本来生成词频云图片的库。

[这是](https://github.com/amueller/word_cloud)它的 GitHub 项目地址，[这是](https://github.com/windard/Python_Lib/blob/master/content/wordcloud.md)我的学习笔记地址。

既然能够生成 词云 ，那么肯定也可以生成 标签云，便将个人博客网站，即[本站](https://windard.com/)的所有文章标题，和简短的文章描述爬取了下来，根据词频制作标签云。在本地爬取，故使用本地的博客地址 `http://127.0.0.1:5002`。

```
# coding=utf-8

import json
import jieba
import requests
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

urls = ['http://127.0.0.1:5002/', 'http://127.0.0.1:5002/opinion/', 'http://127.0.0.1:5002/project/']

result = []

def crawl(url):
    s = requests.get(url)
    content = s.content
    soup = BeautifulSoup(content, 'lxml')
    lists = soup.find('ul', class_='artical-list').find_all('li')
    for li in lists:
        data = {}
        data['title'] = li.find('a').text
        data['desc'] = li.find('div', class_='title-desc').text
        result.append(data)

def show(data):
    text = " ".join([div['title'] + ' ' + div['desc'] for div in data])
    text = " ".join(jieba.cut(text, cut_all=True))

    mask_word = STOPWORDS.union([u'一些', u'一下', u'没有', u'还是', u'但是', u'可以', u'一点'])

    wordcloud = WordCloud(font_path='./msyh.ttc', max_words=66, stopwords=mask_word, width=700, height=400).generate(text)
    plt.imshow(wordcloud)
    plt.axis('off')
    wordcloud.to_file('windard_title_irregular.png')

    wordcloud = WordCloud(max_font_size=30, font_path='./msyh.ttc', stopwords=mask_word, width=700, height=400).generate(text)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file('windard_title_regular.png')

    plt.show()

def main():
    for url in urls:
        crawl(url)
    show(result)

if __name__ == '__main__':
    main()
```

根据词频大小分布

![windard_title_irregular.png](/images/windard_title_irregular.png)

零散分布

![windard_title_regular.png](/images/windard_title_regular.png)

既然可以根据标题和描述生成标签云，那当然也可以根据文章内容来生成。

```
# coding=utf-8

import json
import requests
import urlparse
import jieba
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

host = '127.0.0.1:5002'
urls = ['http://127.0.0.1:5002/']

crawled_urls = []
result = []

def crawl(url):
    s = requests.get(url)
    if s.headers['Content-Type'] != 'text/html; charset=utf-8':
        urls.remove(url)
        return

    content = s.content
    soup = BeautifulSoup(content, 'lxml')
    tags = soup.find_all('a')
    for tag in tags :
        href = urlparse.urljoin(urls[0], tag['href'])
        netloc = urlparse.urlparse(href).netloc
        fragment = urlparse.urlparse(href).fragment
        if netloc != host or href in urls or fragment != '':
            continue
        urls.append(href)
        crawl(href)

def find(url):
    s = requests.get(url)
    content = s.content
    soup = BeautifulSoup(content, 'lxml')
    entry = soup.find("div", class_='entry')
    if not entry:
        return

    data = {}
    data['url'] = url
    data['p'] = [text.text for text in entry.find_all('p')]
    data['h1'] = [text.text for text in entry.find_all('h1')]
    data['h2'] = [text.text for text in entry.find_all('h2')]
    data['h3'] = [text.text for text in entry.find_all('h3')]
    data['h4'] = [text.text for text in entry.find_all('h4')]
    data['h5'] = [text.text for text in entry.find_all('h5')]
    data['h6'] = [text.text for text in entry.find_all('h6')]
    data['ol'] = [text.text for text in entry.find_all('ol')]
    result.append(data)

def show(data):
    text = " ".join(" ".join(div['p']) + " ".join(div['ol']) + " ".join(div['h1']) + " ".join(div['h2']) + " ".join(div['h3']) + " ".join(div['h4']) + " ".join(div['h5']) + " ".join(div['h6']) for div in data)
    text = " ".join(jieba.cut(text))

    mask_word = STOPWORDS.union([u'文件', u'可以', u'一个', u'使用', u'然后', u'什么', u'查看', u'这个', u'如果', u'没有', u'但是', u'或者', u'我们', u'就是', u'需要'])

    wordcloud = WordCloud(font_path='./msyh.ttc', max_words=88, stopwords=mask_word, width=700, height=400).generate(text)
    plt.imshow(wordcloud)
    plt.axis('off')
    wordcloud.to_file('windard_content_irregular.png')

    wordcloud = WordCloud(max_font_size=30, font_path='./msyh.ttc', stopwords=mask_word, width=700, height=400).generate(text)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    wordcloud.to_file('windard_content_regular.png')

    plt.show()

def main():
    crawl(urls[0])
    for url in urls:
        find(url)
    show(result)

if __name__ == '__main__':
    main()

```

根据词频大小分布

![windard_content_irregular.png](/images/windard_content_irregular.png)

零散分布

![windard_content_regular.png](/images/windard_content_regular.png)
