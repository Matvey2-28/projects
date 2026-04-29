
import json

class Parser:
    def __init__(self, data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        self.data = self._clean_json(raw_data)

    def _clean_json(self, item):
        if isinstance(item, dict):
            if 'value' in item:
                val = item['value']
                unit = item.get('unit')
                return (self._clean_json(val), unit.strip()) if unit else self._clean_json(val)
            return {k.strip(): self._clean_json(v) for k, v in item.items()}
        elif isinstance(item, list):
            return [self._clean_json(i) for i in item]
        elif isinstance(item, str):
            return item.strip()
        return item

    def _get_objects_values_by_type(self, obj_type):
        fc = self.data.get('figure_choose', {})
        items = fc.get(obj_type, [])
        result = []
        for item in items:
            obj_values = [item.get('id'), item.get('name_for_object')]
            for key, val in item.items():
                if key not in ['id', 'name_for_object']:
                    # Извлекаем значение и единицу, если есть
                    if isinstance(val, dict):
                        v = val.get('value')
                        u = val.get('unit')
                        if u == 'ae':
                            v *= 1.49e11
                        elif u == 'km':
                            v *= 1000
                        # Можно добавить другие единицы по `config.yaml`
                        obj_values.append(v)
                    else:
                        obj_values.append(val)
            result.append(obj_values)
        return result

    def get_gas_disks(self): return self._get_objects_values_by_type('GAS_DISKS')
    def get_spheres(self): return self._get_objects_values_by_type('SPHERES')
    def get_arbitrary_clusters(self): return self._get_objects_values_by_type('ARBITARY_CLUSTERS')
    def get_material_points(self): return self._get_objects_values_by_type('MATERIAL_POINTS')

    def get_box_size(self):
        box = self.data.get('figure_choose', {}).get('BOX_SIZE')
        return [box] if box is not None else []

    def get_time_period(self):
        td = self.data.get('time_period', {})
        return [td.get('TIME_END'), td.get('DELTA_TIME')]

if __name__ == '__main__':
    p = Parser('input.json')
    print(f"GAS_DISKS: {p.get_gas_disks()}")
    print(f"SPHERES: {p.get_spheres()}")
    print(f"ARBITARY_CLUSTERS: {p.get_arbitrary_clusters()}")
    print(f"MATERIAL_POINTS: {p.get_material_points()}")
    print(f"BOX_SIZE: {p.get_box_size()}")
    print(f"TIME_PERIOD: {p.get_time_period()}")