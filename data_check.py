import os
from xml.etree import ElementTree as ET

# 配置路径（和你的数据集对应）
IMG_DIR = "./NEU-DET/IMAGES"
XML_DIR = "./NEU-DET/ANNOTATIONS"
CLASS_LIST = ["crazing", "inclusion", "patches", "pitted_surface", "rolled-in_scale", "scratches"]

# 1. 统计基础数量
img_list = [f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")]
xml_list = [f for f in os.listdir(XML_DIR) if f.endswith(".xml")]
img_count = len(img_list)
xml_count = len(xml_list)

print(f"=== 基础统计 ===")
print(f"图片总数：{img_count}")
print(f"XML标签总数：{xml_count}")

# 2. 检查图片与XML匹配性
img_names = [os.path.splitext(f)[0] for f in img_list]
xml_names = [os.path.splitext(f)[0] for f in xml_list]

img_no_xml = [name for name in img_names if name not in xml_names]
xml_no_img = [name for name in xml_names if name not in img_names]

print(f"\n=== 匹配性检查 ===")
print(f"有图片无XML的文件：{img_no_xml}，共{len(img_no_xml)}个")
print(f"有XML无图片的文件：{xml_no_img}，共{len(xml_no_img)}个")

# 3. 检查类别标注异常
class_count = {cls: 0 for cls in CLASS_LIST}
unknown_class = []
spell_error = []

for xml_file in xml_list:
    xml_path = os.path.join(XML_DIR, xml_file)
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for obj in root.findall("object"):
        cls_name = obj.find("name").text.strip()
        if cls_name not in CLASS_LIST:
            # 检查拼写错误
            for standard_cls in CLASS_LIST:
                if cls_name.lower() in standard_cls.lower() or standard_cls.lower() in cls_name.lower():
                    spell_error.append((xml_file, cls_name, standard_cls))
                    break
            else:
                unknown_class.append((xml_file, cls_name))
        else:
            class_count[cls_name] += 1

print(f"\n=== 类别统计 ===")
for cls, cnt in class_count.items():
    print(f"{cls}：{cnt}个")

print(f"\n=== 类别异常检查 ===")
print(f"类别拼写错误：{spell_error}，共{len(spell_error)}个")
print(f"未知类别：{unknown_class}，共{len(unknown_class)}个")