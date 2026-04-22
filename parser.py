import json


class Parser:
    
    def __init__(self, data):
        with open(data) as data_file:
            print('Файл загружен.', '\n')
            self.data = json.load(data_file)

    def get_visual_settings(self):
        print('Получены визуальные настройки.')
        data = self.data['visual_settings']
        visual_settings = []
        for parametr in data:
            visual_settings.append(data[parametr]['value'])
        print(visual_settings, '\n')
        return visual_settings


    def get_math_settings(self):
        print('Получены математические настройки.')
        data = self.data['math_settings']
        visual_settings = []
        for parametr in data:
            visual_settings.append(data[parametr]['value'])
        print(visual_settings, '\n')
        return visual_settings


if __name__ == '__main__':
    parser = Parser('input.json')
    a = parser.get_math_settings()
    b = parser.get_visual_settings()
    print()
        