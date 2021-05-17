import time
from datetime import date


class Actions:
    """
    The Actions object contains various info about action/task,
    created by user.

    :param action: used for title of action/task.
    :type action: str
    :param category: used for adding some custom category by user.
    :type category: str
    :param time: used for indicating what time of action/task is.
    :type time: datetime.datetime.time
    :param date: used for indicating what date of action/task is.
    :type date: datetime.datetime.date
    :param duration: used for indicating what duration of action/task is.
    :type duration: int
    :param comment: used for adding some comments to action/task.
    :type comment: str
    """
    def __init__(self, action=None, category=None, \
        hour=None, minute=None, second=None, year=None, month=None, day=None, \
        duration=str, comment=None):

        self.action = action
        self.category = category

        self.hour = hour
        self.minute = minute
        self.second = second

        self.year = year
        self.month = month
        self.day = day
        
        self.duration = duration
        self.comment = comment

        t = f'{self.hour}:{self.minute}:{self.second}'
        time_ = time.strptime(t, '%X')
        self.time = time.strftime('%X', time_)

        date_ = date(self.year, self.month, self.day)
        self.date = date_.strftime('%Y.%m.%d')
    
    def __str__(self):
        pass
                

        