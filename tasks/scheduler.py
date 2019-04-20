from minette.task import Scheduler, Task
from .minute import MinuteTask
from .hour import HourTask


class MyScheduler(Scheduler):
    def register_tasks(self):
        self.schedule.every().minute.do(self.create_task(MinuteTask))
        self.schedule.every().hour.do(self.create_task(HourTask))
