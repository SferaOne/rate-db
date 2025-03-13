import yaml
import json
from transform import YamlTransformer, ResultType

with open('data.v2.yaml') as f:
    data = yaml.safe_load(f)
    transformer = YamlTransformer(data)

jv = open("data.v2.value.json", "w")
jv.write(
    json.dumps(
        transformer.values(ResultType.FLAT), 
        ensure_ascii=False, 
        indent=2)
)

jd = open("data.v2.description.json", "w")
jd.write(
    json.dumps(
        transformer.descriptions(), 
        ensure_ascii=False, 
        indent=2)

)