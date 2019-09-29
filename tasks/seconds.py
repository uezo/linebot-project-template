from minette import Task


class SecondsTask(Task):
    def do(self, **kwargs):
        self.logger.warning("This task runs every 5 seconds")
