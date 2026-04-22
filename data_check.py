import os
from collections import Counter
import xml.etree.ElementTree as ET

# 路径
IMG_DIR = "NEU-DET/images"
XML_DIR = "NEU-DET/annotations"

# 统计
imgs = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
xmls = [f for f in os.listdir(XML_DIR) if f.endswith(".xml")]
print(f"图片总数: {len(imgs)}")
print(f"标注总数: {len(xmls)}")

# 类别统计
classes = []
for xml in xmls:
    tree = ET.parse(os.path.join(XML_DIR, xml))
    for obj in tree.findall("object"):
        classes.append(obj.find("name").text)
print("类别分布:", Counter(classes))