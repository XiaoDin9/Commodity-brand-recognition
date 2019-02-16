# Commodity-brand-recognition
This project is to classify and count the products of Yinlu and Nestle.

The project includes:

    (1) Pre-processing the images of the two brands of Yinlu and Nestle, and converting the format into the format of caffe and tensorflow  input;

    (2) Improve the popular classification and recognition network, SSD and Faster-RCNN neural network, and perform a series of optimizations on the network;

    (3) Using the trained network to predict the test data set, a better result can be obtained.


Organizational structure of the project:

    __  Data preprocessing 文件夹 采用python 编写的一系列图像数据预处理代码

    ——  Dataset 文件夹 使用camera 采集到的银鹭和雀巢两种品牌商品的图片
  
    __  Design network 文件夹 改进的SSD 和 Faster-RCNN网络模型
  
    __  Test and Train network 采用Python 编写的模型测试代码
