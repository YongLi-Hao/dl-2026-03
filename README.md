# YOLOv5从零训练NEU-DET钢材缺陷检测
## 基本信息
- 姓名：【李昊轩】
- YOLO源码仓库：https://github.com/ultralytics/yolov5.git
- 数据集来源：https://github.com/abin24/NEU-DET.git（XML标注原始版本）
- 训练设备：NVIDIA GeForce RTX 5070 Laptop GPU（8G显存）

## 数据转换
python convert_xml_to_yolo.py
原始图片数量：1800
原始 XML 数量：1800
转换后训练集 / 验证集 / 测试集数量：1260 / 360 / 180

## 训练结果
训练总耗时：1.617 小时
batch size：4
img size：640×640
最终 mAP@0.5：0.705
训练曲线路径：./train_results/neu_det_exp3/results.png
预测可视化路径：./train_results/neu_det_exp3/、./visualizations/

## 错误样本分析
本次训练的错误样本主要分为 4 类，对应问题与原因如下：
漏检问题：主要集中在 crazing 裂纹的分支部分、rolled-in_scale 低对比度缺陷、<20×20 像素的 pitted_surface 点蚀。核心原因是从零训练的模型对细微、低对比度特征的学习能力不足，YOLOv5s 下采样过程中小目标特征丢失，导致漏检。
误检问题：钢材表面的正常纹理、光照阴影被误检为 scratches 划痕或 crazing 裂纹。核心原因是正常纹理与缺陷的特征相似度高，从零训练的模型区分正负样本的能力不足，对背景的抗干扰能力弱。
定位偏移问题：crazing 裂纹、scratches 划痕的预测框边界与真实标注存在明显偏移，未完全包裹缺陷。核心原因是细长缺陷的边界模糊，从零训练的模型对目标边界的回归学习不充分，定位精度不足。
小目标失败问题：尺寸小于 32×32 像素的 pitted_surface 点蚀、细小 inclusion 夹杂物大量漏检。核心原因是 YOLOv5s 原生锚框对小目标适配性差，下采样过程中小目标特征被压缩丢失，模型无法捕捉有效特征。

## 源码与环境自检
YOLO 源码获取方式：通过git clone https://github.com/ultralytics/yolov5.git从 GitHub 官方仓库克隆
是否使用pip install ultralytics或conda install ultralytics作为黑盒训练入口：否，全程仅使用源码内的 train.py 作为训练入口，未使用任何黑盒命令
是否使用预训练.pt 权重：否，训练命令显式指定--weights ''，完全从零训练，未使用任何官方 / 第三方预训练权重
env_report.md路径：./env_report.md
neu_det.yaml路径：./neu_det.yaml