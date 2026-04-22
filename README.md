# YOLOv5从零训练NEU-DET钢材缺陷检测
## 一、项目介绍
基于YOLOv5源码，完成东北大学NEU-DET钢材表面缺陷检测任务：
- 不使用预训练权重，从零训练100epoch
- 完成XML标注到YOLO格式的转换
- 配置Conda训练环境，不使用pip/conda安装的黑盒命令

## 二、项目目录结构
dl-2026-03/
├── yolov5/ # 从 GitHub 克隆的 YOLOv5 源码
├── NEU-DET/ # 原始 XML 标注数据集
├── neu_det_yolo/ # 转换后的 YOLO 格式数据集
│ ├── images/
│ │ ├── train/val/test # 训练 / 验证 / 测试集图片
│ └── labels/
│ ├── train/val/test # 对应标签文件
├── convert_xml_to_yolo.py # XML 转 YOLO 格式脚本
├── data_source.md # 数据集核验报告
├── env_report.md # 环境配置报告
├── training_report.md # 训练与错误分析报告
└── README.md # 项目说明

## 三、环境复现
1.  Anaconda Prompt，激活环境：
    conda activate yolo_det
2.  进入 YOLOv5 目录，运行训练命令：
    cd yolov5
    python train.py --data data/neu_det.yaml --cfg models/yolov5s.yaml --weights '' --epochs 100 --batch 16