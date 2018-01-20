from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from news_app.models import *

from apscheduler.schedulers.background import BackgroundScheduler

import newspaper
import os
import time

def scrape_and_insert():
  print("I am Executing!")
  text_threshold = 300
  title_threshold = 5
  print('\nRetrieving Categories...')
  all_categories = Category.objects.all()

  print('\nRetrieved {} Categories...'.format(len(all_categories)))
  new = 0
  for category in all_categories:
    print('\nRetrieved data mines for {}...'.format(category.name))
    data_mines = DataMine.objects.filter(category__name=category.name)
    for mine in data_mines:
      count = 5

      print('\nTrying to build newspaper for {}...'.format(mine.name))
      source_url = mine.source_url
      paper = newspaper.build(source_url, memoize_articles=False)
      print('\nBuilt newspaper for {}'.format(source_url))
      print('\nTrying to parse articles...')

      for article in paper.articles:
        if count == 0:
          break

        try:
          article.download()
          article.parse()
        except newspaper.article.ArticleException:
          print('Failed!')

        title = article.title
        slug = '_'
        text= article.text
        img_url = article.top_image
        source_url = article.url
        print('Parsed 1 new article')

        if not all((title, text, img_url, source_url)):
          continue

        text_is_too_short = len(text) < text_threshold
        title_is_too_short = len(title.split()) < title_threshold

        if text_is_too_short or title_is_too_short:
          continue

        try:
          article_object = Article(title=title, slug=slug, text=text, category=category,
                                   img_url=img_url, source_url=source_url
                                   )
          article_object.save()
          print('Added 1 new article to DB')
          new += 1
          count -= 1
        except IntegrityError:
          continue
  print('{} new articles were added!'.format(new))


class Command(BaseCommand):
  help = 'Scrapes the data mine wesbites specified for news articles.'


  def handle(self, *args, **options):
    scheduler = BackgroundScheduler()
    scheduler.add_job(scrape_and_insert, 'interval', seconds=600)
    scheduler.start()
    self.stdout.write('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
      # This is here to simulate application activity (which keeps the main thread alive).
      while True:
        time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
      # Not strictly necessary if daemonic mode is enabled but should be done if possible
      scheduler.shutdown()

    