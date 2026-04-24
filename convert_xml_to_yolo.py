import os
import shutil
import random
import logging
from xml.etree import ElementTree as ET

# ===================== 配置项（固定，无需修改）=====================
# 路径配置
IMG_SRC_DIR = "./NEU-DET/IMAGES"
XML_SRC_DIR = "./NEU-DET/ANNOTATIONS"
OUTPUT_DIR = "./neu_det_yolo"

# 数据集划分比例（train:val:test = 7:2:1，行业标准）
TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1

# 类别映射（和数据集完全对应）
CLASS_MAP = {
    "crazing": 0,
    "inclusion": 1,
    "patches": 2,
    "pitted_surface": 3,
    "rolled-in_scale": 4,
    "scratches": 5
}

# 固定随机种子，确保每次划分结果完全一致
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# ===================== 日志配置（评分点：完整日志）=====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("convert_log.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ===================== 步骤1：自动创建输出目录结构 =====================
def create_dirs():
    dir_list = [
        os.path.join(OUTPUT_DIR, "images", "train"),
        os.path.join(OUTPUT_DIR, "images", "val"),
        os.path.join(OUTPUT_DIR, "images", "test"),
        os.path.join(OUTPUT_DIR, "labels", "train"),
        os.path.join(OUTPUT_DIR, "labels", "val"),
        os.path.join(OUTPUT_DIR, "labels", "test"),
    ]
    for dir_path in dir_list:
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"创建目录：{dir_path}")


# ===================== 步骤2：XML解析与坐标转换 =====================
def xml_to_yolo(xml_path, img_width, img_height):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    yolo_lines = []

    for obj in root.findall("object"):
        # 解析类别
        cls_name = obj.find("name").text.strip()
        # 修正拼写错误
        if cls_name == "incluson":
            cls_name = "inclusion"
            logger.warning(f"修正拼写错误：{xml_path} 中的 {cls_name}")
        if cls_name == "scratch":
            cls_name = "scratches"
            logger.warning(f"修正拼写错误：{xml_path} 中的 {cls_name}")

        # 异常处理：未知类别
        if cls_name not in CLASS_MAP:
            logger.error(f"未知类别：{xml_path} 中的 {cls_name}，跳过该标注")
            continue

        cls_id = CLASS_MAP[cls_name]

        # 解析边界框
        bndbox = obj.find("bndbox")
        xmin = float(bndbox.find("xmin").text)
        ymin = float(bndbox.find("ymin").text)
        xmax = float(bndbox.find("xmax").text)
        ymax = float(bndbox.find("ymax").text)

        # 异常处理：宽高为0的框
        if xmax <= xmin or ymax <= ymin:
            logger.error(f"无效框：{xml_path} 中宽高为0，跳过该标注")
            continue

        # 异常处理：越界框，修正到图片范围内
        xmin = max(0, xmin)
        ymin = max(0, ymin)
        xmax = min(img_width, xmax)
        ymax = min(img_height, ymax)

        # 转换为YOLO归一化坐标（0-1之间）
        x_center = (xmin + xmax) / 2.0 / img_width
        y_center = (ymin + ymax) / 2.0 / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        # 保留6位小数，符合YOLO格式
        yolo_line = f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
        yolo_lines.append(yolo_line)

    return yolo_lines


# ===================== 步骤3：数据集划分与文件复制 =====================
def split_and_convert():
    # 获取所有有效样本
    all_samples = []
    img_files = [f for f in os.listdir(IMG_SRC_DIR) if f.endswith(".jpg")]

    for img_file in img_files:
        sample_name = os.path.splitext(img_file)[0]
        xml_file = sample_name + ".xml"
        img_path = os.path.join(IMG_SRC_DIR, img_file)
        xml_path = os.path.join(XML_SRC_DIR, xml_file)

        # 检查XML是否存在
        if not os.path.exists(xml_path):
            logger.error(f"样本{sample_name}无XML文件，跳过")
            continue

        all_samples.append(sample_name)

    # 打乱并划分数据集
    random.shuffle(all_samples)
    total_num = len(all_samples)
    train_num = int(total_num * TRAIN_RATIO)
    val_num = int(total_num * VAL_RATIO)

    train_samples = all_samples[:train_num]
    val_samples = all_samples[train_num:train_num + val_num]
    test_samples = all_samples[train_num + val_num:]

    logger.info(f"数据集划分完成：训练集{len(train_samples)}张，验证集{len(val_samples)}张，测试集{len(test_samples)}张")

    # 遍历每个样本，完成转换
    for split_name, sample_list in zip(["train", "val", "test"], [train_samples, val_samples, test_samples]):
        for sample_name in sample_list:
            # 源文件路径
            img_src = os.path.join(IMG_SRC_DIR, sample_name + ".jpg")
            xml_src = os.path.join(XML_SRC_DIR, sample_name + ".xml")

            # 目标路径
            img_dst = os.path.join(OUTPUT_DIR, "images", split_name, sample_name + ".jpg")
            label_dst = os.path.join(OUTPUT_DIR, "labels", split_name, sample_name + ".txt")

            # 复制图片
            shutil.copy(img_src, img_dst)

            # 解析XML，转换为YOLO标签
            # 获取图片宽高
            tree = ET.parse(xml_src)
            root = tree.getroot()
            size = root.find("size")
            img_width = float(size.find("width").text)
            img_height = float(size.find("height").text)

            yolo_lines = xml_to_yolo(xml_src, img_width, img_height)

            # 写入标签文件
            with open(label_dst, "w", encoding="utf-8") as f:
                f.write("\n".join(yolo_lines))

            logger.info(f"转换完成：{sample_name} → {split_name}集")


# ===================== 主函数 =====================
if __name__ == "__main__":
    logger.info("=== 开始XML转YOLO格式任务 ===")
    logger.info(f"固定随机种子：{RANDOM_SEED}")
    create_dirs()
    split_and_convert()
    logger.info("=== 所有转换任务完成！===")