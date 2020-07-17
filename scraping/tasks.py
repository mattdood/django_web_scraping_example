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
        latest_job = Job.objects.filter(source=source).order_by('-id')[0]
        print(latest_job.scraped_pubdate)
    except:
        latest_job = None
        print('var: ', latest_job, 'type: ', type(latest_job))
    
    for j in jobs:
        if latest_job is None:
            try:
                print('job itself: ', j)
                Job.objects.create(
                    title = j['title'],
                    job_description_scraped = j['description'],
                    application_link = j['application_link'],
                    tags = j['category'],
                    scraped_pubdate = j['published'],
                    source = j['source']
                )
                new_count += 1
            except:
                print('failed at latest_job is none')
                continue
        elif latest_job.scraped_pubdate == None:
            try:
                Job.objects.create(
                    title = j['title'],
                    job_description_scraped = j['description'],
                    application_link = j['application_link'],
                    tags = j['category'],
                    scraped_pubdate = j['published'],
                    source = j['source']
                )
                new_count += 1
            except:
                print('failed at latest_job.scraped_pubdate == none')
                continue
        elif latest_job.source == None:
            try:
                Job.objects.create(
                    title = j['title'],
                    job_description_scraped = j['description'],
                    application_link = j['application_link'],
                    tags = j['category'],
                    scraped_pubdate = j['published'],
                    source = j['source']
                )
                new_count += 1
            except:
                print('failed at latest_job.source == none')
                continue
        elif latest_job.scraped_pubdate < j['published']:
            try:
                Job.objects.create(
                    title = j['title'],
                    job_description_scraped = j['description'],
                    application_link = j['application_link'],
                    tags = j['category'],
                    scraped_pubdate = j['published'],
                    source = j['source']
                )
                new_count += 1
            except:
                print('failed at latest_job.scraped_pubdate < j[published]')
                continue
        else:
            return print('job scraping failed, date was more recent than last pubdate')
            # return print('stopped inputing jobs. here are the details: ',
            #              'latest job scraped_pubdate in db: ',
            #              latest_job.scraped_pubdate,
            #              'source of the jobs: ',
            #              j['source'],
            #              'latest job published date from source: ',
            #              j['published'])
    logger.info(f'New jobs: {new_count} job(s) added.')
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
                'created_at': str(datetime.now()),
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
