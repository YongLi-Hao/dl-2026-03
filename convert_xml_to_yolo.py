import os
import xml.etree.ElementTree as ET
import random
import shutil

# 固定配置
SEED = 42
random.seed(SEED)
CLASSES = ["crazing", "inclusion", "patches", "pitted_surface", "rolled-in_scale", "scratches"]
IMG_SRC = "NEU-DET/images"
XML_SRC = "NEU-DET/annotations"
OUTPUT = "neu_det_yolo"

# 创建文件夹
os.makedirs(f"{OUTPUT}/images/train", exist_ok=True)
os.makedirs(f"{OUTPUT}/images/val", exist_ok=True)
os.makedirs(f"{OUTPUT}/images/test", exist_ok=True)
os.makedirs(f"{OUTPUT}/labels/train", exist_ok=True)
os.makedirs(f"{OUTPUT}/labels/val", exist_ok=True)
os.makedirs(f"{OUTPUT}/labels/test", exist_ok=True)

# 转换坐标
def xml2yolo(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[2])/2.0 * dw
    y = (box[1] + box[3])/2.0 * dh
    w = (box[2] - box[0]) * dw
    h = (box[3] - box[1]) * dh
    return (x,y,w,h)

# 划分数据集
xml_files = [f for f in os.listdir(XML_SRC) if f.endswith(".xml")]
random.shuffle(xml_files)
train = xml_files[:1260]
val = xml_files[1260:1620]
test = xml_files[1620:]

# 转换
for split, files in zip(["train","val","test"], [train,val,test]):
    for f in files:
        name = os.path.splitext(f)[0]
        img_path = f"{IMG_SRC}/{name}.jpg"
        tree = ET.parse(f"{XML_SRC}/{f}")
        w = int(tree.find("size/width").text)
        h = int(tree.find("size/height").text)

        # 复制图片
        shutil.copy(img_path, f"{OUTPUT}/images/{split}/{name}.jpg")

        # 生成标签
        with open(f"{OUTPUT}/labels/{split}/{name}.txt", "w") as f:
            for obj in tree.findall("object"):
                cls = obj.find("name").text
                cls_id = CLASSES.index(cls)
                xmlbox = obj.find("bndbox")
                box = (float(xmlbox.find("xmin").text), float(xmlbox.find("ymin").text),
                       float(xmlbox.find("xmax").text), float(xmlbox.find("ymax").text))
                yolo_box = xml2yolo((w,h), box)
                f.write(f"{cls_id} {' '.join(map(str, yolo_box))}\n")

print("✅ 转换完成！生成YOLO格式数据集")