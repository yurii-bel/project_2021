import datetime
import json
import sys
import os
from gui_elements import *

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

    # Next methods was created for changing info about actions.

    def set_categories(self, val):
        self._categories = val

    def set_action(self, val):
        self.__action = val

    def set_category(self, val):
        self.__category = val
    
    def set_time(self, val):
        self.__time = val

    def set_date(self, val):
        self.__date = val

    def set_duration(self, val):
        self.__duration = val

    def set_comment(self, val):
        self.__comment = val

    # Next methods was created for getting info about actions.
    def get_categories(self):
        return self._categories

    def get_action(self):
        return self.__action

    def get_category(self):
        return self.__category
    
    def get_time(self):
        return self.__time

    def get_date(self):
        return self.__date

    def get_duration(self):
        return self.__duration

    def get_comment(self):
        return self.__comment


class MainUI:
    def __init__(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DisplayElements()
    sys.exit(app.exec())