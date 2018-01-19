from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from news_app.models import *

import newspaper

class Command(BaseCommand):
  help = 'Scrapes the data mine wesbites specified for news articles.'
  text_threshold = 150
  title_threshold = 3

  def handle(self, *args, **options):
    # get every min associated with each article
    # scrae the mines for articles. for each article scrape
    # for title text img_url, source_url (article.url)

    self.stdout.write('\nRetrieving Categories...')
    all_categories = Category.objects.all()

    self.stdout.write('\nRetrieved {} Categories...'.format(len(all_categories)))
    new = 0
    for category in all_categories:
      self.stdout.write('\nRetrieved data mines for {}...'.format(category.name))
      data_mines = DataMine.objects.filter(category__name=category.name)
      for mine in data_mines:
        count = 5

        self.stdout.write('\nTrying to build newspaper for {}...'.format(mine.name))
        source_url = mine.source_url
        paper = newspaper.build(source_url, memoize_articles=False)
        self.stdout.write('\nBuilt newspaper for {}'.format(source_url))
        self.stdout.write('\nTrying to parse articles...')

        for article in paper.articles:
          if count == 0:
            break

          try:
            article.download()
            article.parse()
          except newspaper.article.ArticleException:
            self.stdout.write('Failed!')

          title = article.title
          slug = '_'
          text= article.text
          img_url = article.top_image
          source_url = article.url
          self.stdout.write('Parsed 1 new article')

          if not all((title, text, img_url, source_url)):
            continue

          text_is_too_short = len(text) < self.text_threshold
          title_is_too_short = len(title.split()) < self.title_threshold

          if text_is_too_short or title_is_too_short:
            continue

          try:
            article_object = Article(title=title, slug=slug, text=text, category=category,
                                     img_url=img_url, source_url=source_url
                                     )
            article_object.save()
            self.stdout.write('Added 1 new article to DB')
            new += 1
            count -= 1
          except IntegrityError:
            continue


    self.stdout.write('{} new articles were added!'.format(new))