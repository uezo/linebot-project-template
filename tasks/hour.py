from minette.task import Task


class HourTask(Task):
    def do(self, connection):
        self.logger.info("Run every hour task")
