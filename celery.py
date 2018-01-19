import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news.settings')
 
app = Celery('news')
app.config_from_object('django.conf:settings')
 
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
  'scrape-every-10-mins': {
    'task': 'publisher.tasks.send_view_count_report',
    'schedule': crontab(minute='*/10')
  },
}