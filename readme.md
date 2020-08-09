# Building an RSS feed scraper with Python
This is a project created to illustrate the basics of web scraping by pulling information from the [HackerNews RSS feed](https://news.ycombinator.com/rss). This builds from a simple web scraper in `scraping.py`, into an automated scraping tool in `tasks.py`. 

## Articles

1. Building an RSS feed scraper with Python is available [here](https://codeburst.io/building-an-rss-feed-scraper-with-python-73715ca06e1f).

2. Automated web scraping with Python and Celery is available [here](https://codeburst.io/automated-web-scraping-with-python-and-celery-ac02a4a9ce51).

3. Making a web scraping application with Python, Celery, and Django [here]().

## Automated scraping commands
The following are used to start the scheduled scraping with Celery in `tasks.py`.

Starting our RabbitMQ server (terminal #1):
```
rabbitmq-server
```

Starting the scraping and Django app (terminal #2):
```
python manage.py runserver
```

MIT License.