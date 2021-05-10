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
        hour=None, minute=None, year=None, month=None, day=None, \
        duration=str, comment=None):

        self._categories = []

        self.__action = action
        self.__category = category

        self.__hour = hour
        self.__minute = minute

        self.__year = year
        self.__month = month
        self.__day = day
        
        self.__duration = duration
        self.__comment = comment

    # Next methods was created for getting and changing info about actions.
    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, val):
        self.__action = val

    @property
    def category(self):
        return self.__category

    @category.setter
    def category(self, val):
        self.__category = val

    @property
    def hour(self):
        return self.__hour

    @hour.setter
    def hour(self, val):
        self.__hour = val

    @property
    def minute(self):
        return self.__minute

    @minute.setter
    def minute(self, val):
        self.__minute = val

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, val):
        self.__year = val

    @property
    def month(self):
        return self.__month

    @month.setter
    def month(self, val):
        self.__month = val

    @property
    def day(self):
        return self.__day

    @day.setter
    def day(self, val):
        self.__day = val

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, val):
        self.__duration = val

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, val):
        self.__comment = val

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, val):
        self._categories = val

    def __str__(self):
        return f'Название события: {self.__action}' \
                f'Категория: {self.category}' \
                f'Дата: ' \
                f'Время: ' \
                f'Комментарий: {self.comment}'
                

        