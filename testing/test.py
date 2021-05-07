import datetime


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
    def __init__(self, action=None, category=None, time=None, \
        date=None, duration=str, comment=None):

        self._categories = []

        if not isinstance(action, str):
            raise Exception('Name of action must be a string.')
        if not isinstance(category, str):
            raise Exception('For adding your own category, use string type.')

        self.__action = action
        self.__category = category
        self.__time = time
        self.__date = date
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
    def time(self):
        return self.__time

    @time.setter
    def time(self, val):
        self.__time = val

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, val):
        self.__date = val

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
