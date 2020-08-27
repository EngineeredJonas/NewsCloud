from flask import Flask
from flask import render_template
import feedparser
import base64
import io
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud

BBC_FEED = "http://feeds.bbci.co.uk/news/world/rss.xml"
Limit = 4

app = Flask(__name__)


class Article:
    def __init__(self, url, image, title):
        self.url = url
        self.image = image
        self.title = title


def makewordcloud(text):
    pil_img = WordCloud().generate(text=text).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    return img_b64


def parse_article(article_url):  # returns text of given link
    print('Downloading: {}'.format(article_url))
    r = requests.get(article_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ps = soup.find_all('p')
    text = '\n'.join(p.get_text() for p in ps)
    return text


@app.route("/")  # home page
def home():
    feed = feedparser.parse(BBC_FEED)
    articles = []

    for article in feed['entries'][:Limit]:
        text = parse_article(article['link'])
        cloud = makewordcloud(text)
        articles.append(Article(article['link'], cloud, article['title']))

    return render_template('home.html', articles=articles)


if __name__ == '__main__':
    app.run('0.0.0.0')

# https://www.bbc.com/news/10628494#userss -> rss feedparser
# http://feeds.bbci.co.uk/news/world/rss.xml