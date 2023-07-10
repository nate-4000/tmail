import multiprocessing
import os # to check if inbox daemon is running
import psutil # ditto
import inbox # the daemon, just in case we do need to start it

class DaemonException(BaseException):
    def __init__(self):
        super().__init__("Daemon lock file is invalid")

    def __str__(self):
        return self.args[0]

    def __repr__(self):
        return f"DaemonException('{self.args[0]}')"

try:
    x = open(".lock", 'r')
    if psutil.pid_exists(int(x.read())):
        pass
    else:
        raise DaemonException
except (FileNotFoundError, DaemonException):
    print("inbox.py is not running!")
    tinbox = multiprocessing.Process(target=inbox.daemon)
    tinbox.daemon = True
    tinbox.start()


