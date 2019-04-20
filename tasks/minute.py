from minette.task import Task


class MinuteTask(Task):
    def do(self, connection):
        self.logger.info("Run every minute task")
