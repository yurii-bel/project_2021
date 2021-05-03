import datetime
import json

cd = datetime.datetime.now()


class SearchField:
    """
    Description of class SearchField
    """
    def __init__(self):
        self.activity = None
        self.duration = None
        self.date = None
        self.tasks = None
        self.counter = 0
        self.inp = input('Enter activity, duration and date: ')

        self.get_input()
        self.save_to_txt()

    def get_input(self):
        l_inp = list(self.inp)
        task = ''.join(l_inp).split()
        self.activity = task[0]
        self.duration = task[1]
        self.date = task[2]
        self.tasks = {f'{self.counter}': task}

        self.counter += 1

    def save_to_txt(self):
        with open('data.txt', 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    # def update_json(self):
    #     with open("data.txt", "r+") as file:
    #         data = json.load(file)
    #         data.update(self.tasks)
    #         file.seek(0)
    #         json.dump(data, file)

    def __str__(self):
        return f'\nactivity: {self.activity}' \
               f'\nduration: {self.duration}' \
               f'\ndate: {self.date}' \
               f'\ntask: {self.tasks}'


class Diagram:
    """
    Description of class Diagram
    """
    def __init__(self):
        pass


class MainWindow:
    """
    Description of class MainWindow
    """
    def __init__(self):
        pass


if __name__ == '__main__':
    print(SearchField())
