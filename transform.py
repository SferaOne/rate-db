from enum import Enum
from typing import Dict, Any, List


class ResultType(Enum):
    ORIGINAL = 0
    FLAT = 1
    

class YamlTransformer:
    data: Dict

    def __init__(self, data: Dict):
        self.data = data

    def _extract_values(self, data: Dict)-> Dict:
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                if key == "value":
                    if isinstance(value, (dict, list)):
                        extracted = self._extract_values(value)
                        if extracted is not None:  # Игнорируем пустые значения
                            return extracted    
                    else:
                        return value
                elif isinstance(value, (dict, list)):
                    extracted = self._extract_values(value)
                    if extracted is not None:  # Игнорируем пустые значения
                        result[key] = extracted
            return result if result else None
        elif isinstance(data, list):
            return [self._extract_values(item) for item in data if self._extract_values(item) is not None]
        else:
            return None

    def _extract_values_flat(self, data: Dict, parent_key="", separator=".")-> Dict:
        result = {}
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "value":
                    result[parent_key] = value
                elif isinstance(value, (dict, list)):
                    new_key = f"{parent_key}{separator}{key}" if parent_key else key
                    result.update(self._extract_values_flat(value, new_key, separator))
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_key = f"{parent_key}{separator}{index}" if parent_key else str(index)
                result.update(self._extract_values_flat(item, new_key, separator))
        return result

    def _extract_description(self, data):
        if isinstance(data, dict):
            result = {}
            if "desc" in data:
                result["desc"] = data["desc"]
            if "value" in data:
                value = data["value"]
                if isinstance(value, dict):
                    result.update(self._extract_description(value))
                elif isinstance(value, list):
                    result.update({
                        k: v for item in value 
                        for k, v in (self._extract_description(item).items() if isinstance(self._extract_description(item), dict) else {})
                    })
                else:
                    result = data.get("desc", value)
            else:
                for key, val in data.items():
                    if key not in ("desc", "value"):
                        transformed = self._extract_description(val)
                        if transformed:
                            result[key] = transformed
            return result
        elif isinstance(data, list):
            return [self._extract_description(item) for item in data]
        else:
            return data

    def _extract_description_flat(self)-> Dict:
        pass
        

    def values(self, type: ResultType = ResultType.ORIGINAL)-> Dict:
        if type == ResultType.ORIGINAL:
            return self._extract_values(self.data)
        elif type == ResultType.FLAT:
            return self._extract_values_flat(self.data)
        else:
            return self._extract_values(self.data)

    def descriptions(self, type: ResultType = ResultType.ORIGINAL)-> Dict:
        if type == ResultType.ORIGINAL:
            return self._extract_description(self.data)
        elif type == ResultType.FLAT:
            return self._extract_values_flat(self.data)
        else:
            return self._extract_description(self.data)


