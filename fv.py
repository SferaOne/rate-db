import yaml
from collections.abc import MutableMapping

def flatten_yaml(data, parent_key='', sep='.'):
    items = {}
    if isinstance(data, MutableMapping):  # Если data — это словарь
        for key, value in data.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            
            if isinstance(value, MutableMapping):  # Если значение — это словарь
                if 'value' in value:  # Если есть ключ 'value'
                    if isinstance(value['value'], (dict, list)):  # Если значение — это словарь или список
                        items.update(flatten_yaml(value['value'], new_key, sep))
                    else:  # Если значение — это простое значение (строка, число и т.д.)
                        items[new_key] = value['value']
                else:  # Если ключа 'value' нет, рекурсивно обрабатываем словарь
                    items.update(flatten_yaml(value, new_key, sep))
            elif isinstance(value, list):  # Если значение — это список
                for item in value:  # Итерируемся по элементам списка
                    if isinstance(item, MutableMapping):  # Если элемент списка — это словарь
                        items.update(flatten_yaml(item, new_key, sep))
                    else:  # Если элемент списка — это простое значение
                        items[new_key] = item
            else:  # Если значение — это простое значение (строка, число и т.д.)
                items[new_key] = value
    elif isinstance(data, list):  # Если data — это список
        for item in data:  # Итерируемся по элементам списка
            if isinstance(item, MutableMapping):  # Если элемент списка — это словарь
                items.update(flatten_yaml(item, parent_key, sep))
            else:  # Если элемент списка — это простое значение
                items[parent_key] = item
    return items

# Загрузка данных из YAML
with open("data.v2.yaml", "r") as file:
    data = yaml.safe_load(file)

# Разворачиваем структуру
flat = flatten_yaml(data['document']['value'], parent_key='document')

# Фильтрация только нужных полей (без индексов массивов и полей с описанием)
result = {k: v for k, v in flat.items() if not k.endswith('.desc')}

import json
print(json.dumps(result, ensure_ascii=False, indent=2))