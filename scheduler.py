from minette import Scheduler

from task.seconds import SecondsTask


if __name__ == "__main__":
    sc = Scheduler()
    sc.every_seconds(SecondsTask, 5)
    sc.start()
