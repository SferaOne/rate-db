import yaml
from typing import Dict, Any, List


doc = {}


def _get_val_key(is_value: bool = True):
    if is_value:
        return "value"
    else:
        return "desc"
    
def _get_node_item(node: Dict, item: Any, key: str)-> Any:
    if isinstance(node[item].get(key), dict):
        return node[item].get(key)
    elif isinstance(node[item].get(key), str):
        return node[item].get(key)
    elif isinstance(node[item].get(key), list):
        return node[item].get(key)
    else:
        return node[item].get(key)

def parse_node_list(node: List, is_value: bool = True):
    key = _get_val_key(is_value)
    for item in node:
        try:
            if isinstance(item, dict):
                if item.get(key) is not None:
                    print(f"------{item.get(key)}")
                else:
                    parse_node(item)
        except:
            pass

def parse_node(node: Dict, root: str = "", is_value: bool = True):
    key = _get_val_key(is_value)
    for item in node:
        n = _get_node_item(node, item, key)
        if isinstance(n, dict):
            root = item
            parse_node(n, item, is_value)
        elif isinstance(n, str):
            print(f"---{root}.{item} = {n}")
        elif isinstance(n, list):
            print(item)
            parse_node_list(n, is_value)
        else:
            print(f"---{root}.{item} = {n}")

with open('data.v2.yaml') as f:
    data = yaml.safe_load(f)

parse_node(data)
print(doc)