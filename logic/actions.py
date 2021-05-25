import datetime

from PyQt5.QtCore import QDate


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
    def __init__(self, action=str, category=str, date=QDate,\
        duration=str, comment=str):

        self.action = action
        self.category = category
        self.duration = duration
        self.comment = comment

        self.date_ = datetime.date(date.year(), date.month(), date.day())
        self.date = self.date_.strftime('%Y-%m-%d')
    
    def __str__(self):
        return self.date
        