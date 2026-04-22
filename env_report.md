# YOLOv5 训练环境配置报告
## 一、环境基本信息
- 操作系统：Windows 11
- 环境管理工具：Miniconda
- Conda环境名：`yolo_det`
- Python版本：3.10
- PyTorch版本：2.5.1（GPU版，支持CUDA 11.8）
- 硬件设备：NVIDIA GeForce RTX 5070 Laptop GPU（8GB显存）

## 二、环境搭建步骤
### 1. 创建并激活Conda环境
# Anaconda Prompt运行
conda create -n yolo_det python=3.10 -y
conda activate yolo_det
### 2.安装 GPU 版 PyTorch
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
### 3.验证 GPU 可用性
python -c "import torch; print(torch.cuda.is_available())"
# 输出结果：True（表示GPU可用）
### 4.安装 YOLOv5 依赖
cd yolov5
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple