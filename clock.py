from apscheduler.schedulers.blocking import BlockingScheduler
from engine import *

sched = BlockingScheduler()

@sched.scheduled_job('interval',seconds=20)
def timed_job():
  main()
  return


sched.start()
