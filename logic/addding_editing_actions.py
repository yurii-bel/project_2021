from datetime import datetime

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

        self.categories = []

        if not isinstance(action, str):
            raise Exception('Name of action must be a string.')
        if not isinstance(category, str):
            raise Exception('For adding your own category, use string type.')

        self.action = action
        self.category = category
        self.time = time
        self.date = date
        self.duration = duration
        self.comment = comment

    # Next methods was created for changing info about actions.
    def set_categories(self, val):
        self.categories = val

    def set_action(self, val):
        self.action = val

    def set_category(self, val):
        self.category = val
    
    def set_time(self, val):
        self.time = val

    def set_date(self, val):
        self.date = val

    def set_duration(self, val):
        self.duration = val

    def set_comment(self, val):
        self.comment = val


# tests.
# if __name__ == '__main__':
#     a = Actions('Gaming on PC', 'Chill', None, None, 3, 'Lol!')
#     print(a.category)