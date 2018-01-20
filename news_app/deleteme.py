"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""
import newspaper

url = 'http://edition.cnn.com'

n = newspaper.build(url)
count = 1
for i in n.articles:
  if count== 5:
    break
  print(i.url)
  count += 1
# from datetime import datetime
# import time
# import os

# from apscheduler.schedulers.background import BackgroundScheduler


# def tick():
#   print('Tick! The time is: %s' % datetime.now())


# if __name__ == '__main__':
#   scheduler = BackgroundScheduler()
#   scheduler.add_job(tick, 'interval', seconds=300)
#   scheduler.start()
#   print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

#   try:
#     # This is here to simulate application activity (which keeps the main thread alive).
#     while True:
#         time.sleep(5)
#   except (KeyboardInterrupt, SystemExit):
#     # Not strictly necessary if daemonic mode is enabled but should be done if possible
#     scheduler.shutdown()