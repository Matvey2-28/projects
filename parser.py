import json


class Parser:
    
    def __init__(self, data):
        with open(data) as data_file:
            print('Файл загружен.', '\n')
            self.data = json.load(data_file)

    def get_physical_settings(self):
        print('Получены физические настройки.')
        data = self.data['figure_choose']
        visual_settings = []
        for parametr in data:
            visual_settings.append(data[parametr]['value'])
        print(visual_settings, '\n')
        return visual_settings



if __name__ == '__main__':
    parser = Parser('input.json')
    a = parser.get_physical_settings()
    print()
        