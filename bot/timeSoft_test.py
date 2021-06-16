import re
import string

from datetime import datetime


class InputCheck:
    """
    The InputCheck class implements base checking system for various input data.

    Attributes:
        input_text (str):The string which can be checked using various methods.
    """

    def __init__(self, input_text):
        self.text = input_text

        self.correct_rus_vals = []
        # TODO: Добавить еще 1030, 1031, 1111, 1100
        # Appending correct_rus_vals with lower and upper case russian symbols.
        for i in range(1040, 1104):
            self.correct_rus_vals.append(chr(i))

        # List contains codes of correct symbols.
        self.correct_vals = list(string.ascii_lowercase)
        self.correct_vals_with_num = self.correct_vals + \
            ['_'] + [str(x) for x in range(0, 10)]

        # TODO: избавиться от only_in_quotes
        self.only_in_quotes_char = ['!', ',', ':']
        self.incorrect_vals = ['"', '\'', '/', '\\', ',', '--', ';']

    def check_email(self):
        """
        This method makes various checks for correct email.
        If the email passes verification, it returns True(bool) only.
        If not passes, it returns list that contains two values:
        False(bool) and error message(str).

        Returns:
            True | [False | err_msg]
        """

        # Check for the number of "@" characters.
        if self.text.count('@') > 1 or self.text.count('@') == 0:
            return [False, 'Неверное количество знаков "@".']

        # Check for domain length.
        [name, domain] = self.text.split('@')
        if len(domain) < 3:
            return [False, 'Доменное имя короче 3 символов.']
        if len(domain) > 60:
            return [False, 'Доменное имя длиннее 60 символов.']
        if domain.count('.') == 0:
            return [False, 'Доменное имя не содержит точки.']

        # Domain check.
        includedomain = domain.split('.')
        self.correct_vals.extend(['-', '_'])
        for k in includedomain:
            # Checking if there are empty substrings in the domain.
            if k == '':
                return [False, 'Доменное имя содержит пустую строку между точками.']
            # Checking if there are any illegal characters in substrings
            # of the domain.
            for n in k:
                if n not in self.correct_vals:
                    return [False, f'Недопустимый символ {n}']
            if (k[0] == '-') or (k[len(k)-1] == '-'):
                return [False, 'Доменное имя не может начинаться/заканчиваться знаком "-".']
        if len(name) > 60:
            return [False, 'Имя почты длиннее 60 символов.']

        # Add to the list of valid characters (; " ! : ,).
        self.correct_vals_with_num.extend(self.only_in_quotes_char)
        self.correct_vals_with_num.extend(['.', ';', '"'])
        # Checking for double quotes.
        if name.count('"') % 2 != 0:
            return [False, 'Непарные кавычки.']
        # Variables to track period and opening quotes.
        doubledot = False
        inquotes = False
        for k in name:
            if k == '"':
                inquotes = not inquotes
            if k in self.only_in_quotes_char and not inquotes:
                return [False, 'Недопустимый символ вне кавычек.']
            if k not in self.correct_vals_with_num:
                return [False, f'Недопустимый символ. "{k}"']
            # Checking for two points in a row.
            if k == '.':
                if doubledot:
                    return [False, 'Две точки в названии почты.']
                else:
                    doubledot = True
        return True

    def check_date(self):
        # checking date and its format.
        if self.text.isdigit():
            if int(self.text) > (datetime.now() - datetime(year=1900, month=1, day=1)).days - 1:
                return [False, 'Введённое количество дней указывает на дату ранее 1900 года.']
        elif len(self.text.split(', ')) in range(1, 3):
            for x in self.text.split(', '):
                if not re.match(r"^(0[1-9]|[12][0-9]|3[01])[.](0[1-9]|1[012])[.](19|20)\d\d$", x):
                    try:
                        if datetime.strptime(self.text, '%d.%m.%Y') > datetime.now():
                            return [False, 'Дата должна не может быть больше сегодняшней ({0}).'.format(
                                datetime.now().strftime('%d.%m.%Y'))]
                    except Exception:
                        return [False, 'Неверный формат даты.']
                    return [False, 'Неверный формат даты.']
        return True
