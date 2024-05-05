import xml.etree.ElementTree as ET
from tqdm import tqdm

changeset_file = "E:\\Download\\changesets-240219.osm\\changesets-240219.osm"
count = 0
with open(changeset_file, "rb") as f:
    # 创建 XML 解析器
    context = ET.iterparse(f, events=("start",))
    for event, elem in tqdm(context):
        if elem.tag == 'changeset':
            row_data = {}
            for key, value in elem.attrib.items():
                row_data[key] = value
