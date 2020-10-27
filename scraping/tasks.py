# tasks
from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import app, shared_task

# job model
from .models import News

# scraping
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import lxml

# logging
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# save function
@shared_task(serializer='json')
def save_function(article_list):
    """Save articles to the database.

    Saves articles to the database if they do not already exist.

    Parameters:
        article_list (json, str): A JSON list of article objects.
    Returns:
        News (class News): Article objects for each unique article.
    """
    source = article_list[0]['source']
    new_count = 0

    error = True
    try: 
        latest_article = News.objects.filter(source=source).order_by('-id')[0]
        print(latest_article.published)
        print('var TestTest: ', latest_article, 'type: ', type(latest_article))
    except Exception as e:
        print('Exception at latest_article: ')
        print(e)
        error = False
        pass
    finally:
        # if the latest_article has an index out of range (nothing in model) it will fail
        # this catches failure so it passes the first if statement
        
        if error is not True:
            latest_article = None

    for article in article_list:

        # latest_article is None signifies empty DB
        if latest_article is None:
            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except Exception as e:
                print('failed at latest_article is none')
                print(e)
                break
        
        # latest_article.published date < article['published']
        # halts the save, to avoid repetitive DB calls on already existing articles
        elif latest_article.published < article['published']:
            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except:
                print('failed at latest_article.published < j[published]')
                break
        else:
            return print('news scraping failed')

    logger.info(f'New articles: {new_count} articles(s) added.')
    return print('finished')

# scraping function
@shared_task
def hackernews_rss():
    """Scraping function for HackerNews.

    Executes web scraping using the `requests` library
    to parse XML from the HackerNews RSS feed.

    Parameters:
        None
    Returns:
        article_list (JSON, str): A JSON list of articles.
    """
    article_list = []

    try:
        print('Starting the scraping tool')
        # execute my request, parse the data using XML
        # parser in BS4
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, features='xml')

        # select only the "items" I want from the data
        articles = soup.findAll('item')

        # for each "item" I want, parse it into a list
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published_wrong = a.find('pubDate').text
            published = datetime.strptime(published_wrong, '%a, %d %b %Y %H:%M:%S %z')

            # create an "article" object with the data
            # from each "item"
            article = {
                'title': title,
                'link': link,
                'published': published,
                'source': 'HackerNews RSS'
            }

            # append my "article_list" with each "article" object
            article_list.append(article)
        
        print('Finished scraping the articles')

        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)
