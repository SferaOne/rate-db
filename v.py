import yaml
import json

def extract_values_only(data):
    result = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "value":
                if isinstance(value, str):
                    result.append(value)
                elif isinstance(value, (dict, list)):
                    result.extend(extract_values_only(value))
    elif isinstance(data, list):
        for item in data:
            result.extend(extract_values_only(item))
    return result


with open('data.v2.yaml') as f:
    data = yaml.safe_load(f)
# Извлечение значений
values_only = extract_values_only(data)

# Преобразование в JSON
json_values_only = json.dumps(values_only, ensure_ascii=False, indent=2)
print(json_values_only)