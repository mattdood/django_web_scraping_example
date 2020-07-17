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

# logging
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# save function
@shared_task(serializer='json')
def save_function(article_list):
    print('starting')
    source = article_list[0]['source']
    new_count = 0
    print(source)
    try: 
        latest_article = News.objects.filter(source=source).order_by('-id')[0]
        print(latest_article.published)
    except:
        latest_article = None
        print('var: ', latest_article, 'type: ', type(latest_article))
    
    for article in article_list:
        if latest_article is None:
            try:
                print('news itself: ', article)
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except:
                print('failed at latest_job is none')
                continue
        elif latest_article.published == None:
            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except:
                print('failed at latest_job.scraped_pubdate == none')
                continue
        elif latest_article.source == None:
            try:
                News.objects.create(
                    title = article['title'],
                    link = article['link'],
                    published = article['published'],
                    source = article['source']
                )
                new_count += 1
            except:
                print('failed at latest_job.source == none')
                continue
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
                print('failed at latest_job.scraped_pubdate < j[published]')
                continue
        else:
            return print('news scraping failed, date was more recent than last published date')

    logger.info(f'New articles: {new_count} articles(s) added.')
    return print('finished')

# scraping function
@shared_task
def hackernews_rss():
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
            published = a.find('pubDate').text

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
        # after the loop, dump my saved objects into a .txt file
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)
