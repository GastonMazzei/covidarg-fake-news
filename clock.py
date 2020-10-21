from apscheduler.schedulers.blocking import BlockingScheduler
from app.engine import *
import os

sched = BlockingScheduler()

@sched.scheduled_job('interval',seconds=20)
def timed_job():
  print('RUN!')
  cdir = os.getcwd()
  os.chdir('app')  
  main()
  os.chdir(cdir)
  return


sched.start()
