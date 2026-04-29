import json

class Parser:
    def __init__(self, data):

        with open(data, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        self.data = self._clean_json(raw_data)

    def _clean_json(self, item):

        if isinstance(item, dict):

            if 'value' in item:
                val = item['value']
                unit = item.get('unit')

                if unit:
                    return (self._clean_json(val), unit.strip())
                return self._clean_json(val)
            

            return {k.strip(): self._clean_json(v) for k, v in item.items()}
        elif isinstance(item, list):

            return [self._clean_json(i) for i in item]
        elif isinstance(item, str):
            return item.strip()
        return item

    def _get_objects_values_by_type(self, obj_type):
      
        fc = self.data.get('figure_choose', {})
        items = fc.get(obj_type, [])
        
        all_objects_values = []
        
        for item in items:

            obj_values = [
                item.get('id'),             
                item.get('name_for_object') 
            ]


            for key, val in item.items():
                if key not in ['id', 'name_for_object']:
                    obj_values.append(val)
            
            all_objects_values.append(obj_values)
            
        return all_objects_values

    def get_gas_disks(self):

        lists = self._get_objects_values_by_type('GAS_DISKS')
        for lst in lists:
            print(lst)

    def get_spheres(self):
      
        lists = self._get_objects_values_by_type('SPHERES')
        for lst in lists:
            print(lst)

    def get_arbitrary_clusters(self):
        lists = self._get_objects_values_by_type('ARBITARY_CLUSTERS')
        for lst in lists:
            print(lst)

    def get_material_points(self):
        lists = self._get_objects_values_by_type('MATERIAL_POINTS')
        for lst in lists:
            print(lst)

    def get_box_size(self):
        box_size = self.data.get('figure_choose', {}).get('BOX_SIZE')
        if box_size is not None:
            print([box_size])
        else:
            print([])

    def get_time_period(self):

        time_data = self.data.get('time_period', {})
        time_end = time_data.get('TIME_END')
        delta_time = time_data.get('DELTA_TIME')

        print([time_end, delta_time])

if __name__ == '__main__':
    parser = Parser('input.json')
    
    parser.get_gas_disks()
    parser.get_spheres()
    parser.get_arbitrary_clusters()
    parser.get_material_points()
    parser.get_box_size()
    parser.get_time_period()