import itertools

from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):

  name = models.CharField(max_length=50, unique=True)

  def __str__(self):
    return self.name.capitalize()

  def get_absolute_url(self):
    return reverse('news_app:category_articles', kwargs={'category':self.name})

  def save(self, *args, **kwargs):
    self.name = self.name.lower()
    super(Category, self).save(*args, **kwargs)

  class Meta:
    verbose_name_plural = 'Categories'


class Article(models.Model):

  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=50)
  text = models.TextField()
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  img_url = models.CharField(max_length=200)
  source_url = models.CharField(max_length=200)
  keywords = models.CharField(max_length=250)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('news_app:detail', kwargs={'slug': self.slug, 'id':self.id})

  def save(self, *args, **kwargs):
    '''
    Courtesy of https://keyerror.com/blog/automatically-generating-unique-slugs
    -in-django
    '''
    max_length = Article._meta.get_field('slug').max_length
    self.slug = orig = slugify(self.title)[:max_length]

    if Article.objects.filter(slug=self.slug).exists():
      for x in itertools.count(1):
        if not Article.objects.filter(slug=self.slug).exists():
          break

        # Truncate the original slug dynamically. Minus 1 for the hyphen.
        self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

    super(Article, self).save(*args, **kwargs)


class DataMine(models.Model):

  name = models.CharField(max_length=200)
  source_url = models.CharField(max_length=200)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  date_created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name
