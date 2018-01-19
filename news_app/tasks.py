from django.template import Template, Context
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from news.celery import app
from news_app.models import Category, Article
 
import newspaper
 
REPORT_TEMPLATE = """
Here's how you did till now:
 
{% for post in posts %}
        "{{ post.title }}": viewed {{ post.view_count }} times |
 
{% endfor %}
"""
 
 
@app.task
def scrape_news_sites():
  text_threshold = 150
  title_threshold = 3

  # get every min associated with each article
  # scrae the mines for articles. for each article scrape
  # for title text img_url, source_url (article.url)

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

        text_is_too_short = len(text) < self.text_threshold
        title_is_too_short = len(title.split()) < self.title_threshold

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