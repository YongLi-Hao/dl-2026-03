# YOLOv5 训练环境配置报告
## 一、环境基本信息
操作系统：Windows 11
Anaconda 版本：conda 23.10.0
Python 版本：3.10.20
虚拟环境名称：yolo_det
训练设备：NVIDIA GeForce RTX 5070 Laptop GPU（8151MiB）
PyTorch 版本：2.5.1
CUDA 版本：适配 PyTorch 2.5.1

## 二、YOLO 源码获取（合规性说明）
git clone https://github.com/ultralytics/yolov5.git

## 三、环境搭建步骤
### 1. 创建并激活Conda环境
# 创建虚拟环境
conda create -n yolo_det python=3.10 -y
# 激活环境
conda activate yolo_det
# 验证Python版本
python --version
### 2.安装 GPU 版 PyTorch
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
### 3.验证 GPU 可用性
python -c "import torch; print(torch.cuda.is_available())"
# 输出结果：True（表示GPU可用）
### 4.安装 YOLOv5 依赖
cd yolov5
pip install -r requirements.txt

## 四、训练入口说明
训练入口脚本：yolov5/train.py
核心参数说明：
--data：指定自定义的neu_det.yaml数据集配置文件
--epochs：训练轮次（GPU 100）
--weights：预训练权重，设置为''实现从零训练
--cfg：从零训练需指定的模型结构配置文件（models/yolov5s.yaml）
--device：训练设备（GPU 填 0）

## 五、数据集配置文件neu_det.yaml

## 六、报错与修复记录
# 报错内容：ModuleNotFoundError: No module named 'ultralytics'	
报错原因：手动卸载了 ultralytics 包，导致源码运行缺少依赖	
解决方案：从 YOLOv5 源码自带的requirements.txt重新安装依赖
# 报错内容：'tee' 不是内部或外部命令	
报错原因:Windows CMD 不支持 Linux 的 tee 命令	
解决方案:去掉日志重定向后缀，直接执行训练命令
# 报错内容：FileNotFoundError: [Errno 2] No such file or directory: ''	
报错原因:从零训练设置--weights ''时，未指定模型结构配置文件--cfg	
解决方案:训练命令添加--cfg models/yolov5s.yaml