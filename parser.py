import json

class Parser:
    def __init__(self, file_path):
        """Загружает файл и очищает данные."""
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # Очищаем данные: убираем пробелы, извлекаем значения из {"value": ...}
        self.data = self._clean_json(raw_data)

    def _clean_json(self, item):
        """Рекурсивная очистка JSON."""
        if isinstance(item, dict):
            # Если это обертка {"value": 10, "unit": "ae"}
            if 'value' in item:
                val = item['value']
                unit = item.get('unit')
                # Если есть единица измерения, возвращаем кортеж (значение, единица), иначе просто значение
                if unit:
                    return (self._clean_json(val), unit.strip())
                return self._clean_json(val)
            
            # Обычный словарь: чистим ключи и значения
            return {k.strip(): self._clean_json(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [self._clean_json(i) for i in item]
        elif isinstance(item, str):
            return item.strip()
        return item

    def get_objects_as_value_lists(self):
        """
        Возвращает список объектов, где каждый объект — это СПИСОК значений.
        Формат: [ [id, name, val1, val2, ...], [id, name, val1, ...], ... ]
        Названия параметров (ключи) убраны.
        """
        fc = self.data.get('figure_choose', {})
        all_objects_values = []

        # Порядок типов объектов
        obj_types = ['GAS_DISKS', 'SPHERES', 'ARBITARY_CLUSTERS', 'MATERIAL_POINTS']

        for obj_type in obj_types:
            items = fc.get(obj_type, [])
            for item in items:
                # Начинаем список значений с ID и Имени
                obj_values = [
                    item.get('id'),       # ID
                    item.get('name_for_object') # Name
                ]

                # Добавляем остальные значения в том порядке, в котором они идут в словаре
                # (В Python 3.7+ порядок ключей сохраняется)
                for key, val in item.items():
                    if key not in ['id', 'name_for_object']:
                        # Убираем префикс из ключа для логики, но в список кладем только значение
                        obj_values.append(val)
                
                all_objects_values.append(obj_values)

        return all_objects_values

    def print_summary(self):
        """Выводит результаты в виде списков значений."""
        objects_lists = self.get_objects_as_value_lists()
        
        print("--- СПИСКИ ЗНАЧЕНИЙ ОБЪЕКТОВ (без ключей) ---")
        print(f"Всего объектов: {len(objects_lists)}\n")
        
        for i, obj_list in enumerate(objects_lists):
            # obj_list выглядит как: [id, name, val1, val2, ...]
            print(f"Объект #{i+1}: {obj_list}")
        
        # Также выведем BOX_SIZE и TIME отдельно
        box_size = self.data.get('figure_choose', {}).get('BOX_SIZE')
        time_end = self.data.get('time_period', {}).get('TIME_END')
        delta_time = self.data.get('time_period', {}).get('DELTA_TIME')
        
        print(f"\nBOX_SIZE значение: {box_size}")
        print(f"TIME параметры: [End: {time_end}, Dt: {delta_time}]")

if __name__ == '__main__':
    parser = Parser('input.json')
    
    # Получаем список списков значений
    data_lists = parser.get_objects_as_value_lists()
    
    # Вывод на экран
    parser.print_summary()
    
    # Пример доступа к данным:
    