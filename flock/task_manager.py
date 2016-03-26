from multiprocessing import Queue
from threading import Thread

class TaskManager():

    def __init__(self):
        self.task_queue = Queue()
        self.running = True
        Thread(target=self._run).start()

    def _run(self):
        while self.running:
            task = self.task_queue.get(True)
            print 'Running Task %s' % task

            if task['action'] == 'invite':
                self._send_invite(task)

            if task['action'] == 'quit':
                pass

    def _send_invite(self, task):
        print 'Sending Invite'
        print task

    def push(self, task):
        self.task_queue.put(task)

    def stop(self):
        self.running = False
        self.task_queue.put({'action': 'quit'})
