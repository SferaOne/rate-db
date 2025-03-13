#   This work fine

def extract_descriptions_with_paths(data, path=""):
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            if key == "desc":
                # Если это значение "desc", сохраняем его с путем
                result[new_path] = value
            elif isinstance(value, (dict, list)):
                # Рекурсивно обрабатываем вложенные структуры
                extracted = extract_descriptions_with_paths(value, new_path)
                if extracted:  # Игнорируем пустые значения
                    result.update(extracted)
        return result if result else None
    elif isinstance(data, list):
        # Обрабатываем списки
        result = {}
        for index, item in enumerate(data):
            new_path = f"{path}[{index}]"
            extracted = extract_descriptions_with_paths(item, new_path)
            if extracted:  # Игнорируем пустые значения
                result.update(extracted)
        return result if result else None
    else:
        # Игнорируем простые значения (не словари и не списки)
        return None
    
_____________________________

#   This not tested

def extract_descriptions_flat(data, path=""):
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            if key == "desc":
                # Если это значение "desc", сохраняем его с путем
                result[new_path] = value
            elif isinstance(value, (dict, list)):
                # Рекурсивно обрабатываем вложенные структуры
                extracted = extract_descriptions_flat(value, new_path)
                if extracted:  # Игнорируем пустые значения
                    result.update(extracted)
        return result if result else None
    elif isinstance(data, list):
        # Обрабатываем списки
        result = {}
        for index, item in enumerate(data):
            new_path = f"{path}[{index}]"
            extracted = extract_descriptions_flat(item, new_path)
            if extracted:  # Игнорируем пустые значения
                result.update(extracted)
        return result if result else None
    else:
        # Игнорируем простые значения (не словари и не списки)
        return None
    
_____________________________
def extract_values_flat(data, parent_key="", separator="."):
    result = {}
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "value":
                # Если это поле "value", сохраняем его значение
                result[parent_key] = value
            elif isinstance(value, (dict, list)):
                # Формируем новый путь без упоминания "value"
                new_key = f"{parent_key}{separator}{key}" if parent_key else key
                # Рекурсивно обрабатываем вложенные структуры
                result.update(extract_values_flat(value, new_key, separator))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_key = f"{parent_key}{separator}{index}" if parent_key else str(index)
            result.update(extract_values_flat(item, new_key, separator))
    return result