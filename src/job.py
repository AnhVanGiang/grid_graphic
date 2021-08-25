import threading
import time


class Job(threading.Thread):
    """
    https://topic.alibabacloud.com/a/python-thread-pause-resume-exit-detail-and-example-_python_1_29_20095165.html
    """
    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self._flag = threading.Event()  # The flag used to pause the thread
        self._flag.set()  # Set to True
        self._running = threading.Event()  # Used to stop the thread identification
        self._running.set()  # Set running to True

    def run(self):
        while self._running.isSet():
            self._flag.wait()

    def pause(self):
        self._flag.clear()  # Set to False to block the thread

    def resume(self):
        self._flag.set()  # Set to True, let the thread stop blocking

    def stop(self):
        self._flag.set()  # Resume the thread from the suspended state, if it is already suspended
        self._running.clear()  # Set to False

