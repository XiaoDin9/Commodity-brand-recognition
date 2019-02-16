# -*- coding: utf-8 -*-
import tensorflow as tf
import cv2
import glob
import os
from PIL import Image

picture_dir = "./source_data_files/xiaocheshurentou/img"  # 图片的地址
label_file = "./source_data_files/xiaocheshurentou/images_list.label"        #label文件的地址

def image_list():
    # 获取当前目录下所有的有效图片文件。
    extensions = ['png', 'jpeg','jpg']
    file_list = []

    for extension in extensions:
        file_glob = os.path.join(picture_dir, '*.' + extension)
        file_list.extend(glob.glob(file_glob))
        if not file_list:
            continue

    #处理目录下的图片文件,file_list = ['xxx.jpeg','xxx1.jpeg',....]
    filter_label_file(file_list)


def filter_label_file(file_list):   #picture_list = ./source_data_files/B_picture_file/img\\xxx.jpeg,......

    # 产生的picture_list中包含有B29T00下的所有图片列表
    picture_list = []
    for i in range(0, len(file_list)):
        aa = []
        for j in file_list[i].split('\\'):  # ./picture\\B29T00\\20170706012121.jpeg
            aa.append(j)
        picture_list.append(aa[1])

    cc = []
    dd = []
    num = 0
    label_list = []
    file_name = []
    #处理标签文件
    with open(label_file, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()  #整行读取数据
            if not lines:
                break

            #提取出标签中的图片名行,lines = img/B57T18_20170706062248.jpeg
            if lines[0] == 'i':    #图片的路径信息
                dd = []
                bb = []
                cc = []

                for k in lines.split('/'):
                    bb.append(k)                #bb = ['img','B29T00_20170706012121.jpeg/n']
                for x in bb[1].split('\n'):
                    dd.append(x)

                for j in dd[0].split('.'):        #dd[0] = 'B29T00_20170706012121.jpeg'
                    cc.append(j)                   #cc[0] = 'B29T00_20170706012121'
                continue

            #处理数字行
            if int(len(lines)) == 2:
                num = int(lines)
                if num ==0:
                    continue
                else:
                    label_list = []
                    file_name = []
                    # 创建.txt文件
                    file_name = cc[0] + ".txt"
                    create_txt_file(file_name, num, "\n")

                    #处理图片标签位置信息
                    for i in range(0,num):
                        lines = file_to_read.readline()
                        if not lines:
                            break
                        else:
                            mm = []
                            for l in lines.split(','):
                                mm.append(l)                  # mm = ['-1','23','233','432']
                        label_list.append(mm)

                    #调用匹配函数
                    pipei_fun(picture_dir, label_list, file_name, dd[0], cc[0])

def create_txt_file(file_name, num, qq):
    with open(file_name, 'a') as file:
        file.write(str(num) + qq)

def pipei_fun(picture_dir, label_list, file_name, dd, cc):

    picture = os.path.join(picture_dir,dd)
    image = cv2.imread(picture)

    xmin = []
    ymin = []
    xmax = []
    ymax = []

    for j in range(0,len(label_list)):
        xmin.append(int(label_list[j][0]))
        ymin.append(int(label_list[j][1]))
        xmax.append(int(label_list[j][2]))
        ymax.append(int(label_list[j][3]))

    #扩展图片的边界,返回坐标信息
    xmin1, ymin1, xmax1, ymax1 = expand_bbox(image, xmin, ymin, xmax, ymax,cc)
    cv2.imwrite(os.path.join('./source_data_files/', cc + ".jpg"), image)

    #把更改后的坐标值写到.txt文件中去
    for i in range(0,len(xmax1)):
        create_txt_file(file_name, xmin1[i], " ")
        create_txt_file(file_name, ymin1[i], " ")
        create_txt_file(file_name, xmax1[i], " ")
        create_txt_file(file_name, ymax1[i], "\n")

def expand_bbox(image, xmin, ymin, xmax, ymax,cc):

    #剪切之后还需要扩展下边部分当有需要时按照roi扩充
    ex_t = 0        #扩展上面
    ex_l = 0        #扩展左边
    ex_r = 0        #扩展右边
    ex_b = 0        #扩展下面

    flag = False

    sp = image.shape
    #print(sp[1], sp[0])
    image_cols = int(sp[1])
    image_rows = int(sp[0])

    for i in range(0,len(xmin)):
        if xmin[i] < 0:
            number = xmin[i]
            for j in range(0,len(xmin)):
                xmin[j] = xmin[j] + abs(number)
                xmax[j] = xmax[j] + abs(number)
            flag = True
            ex_l = ex_l + abs(number)

    for i in range(0, len(ymin)):
        if ymin[i] < 0:
            number = ymin[i]
            for j in range(0, len(ymin)):
                ymin[j] = ymin[j] + abs(number)
                ymax[j] = ymax[j] + abs(number)
            flag = True
            ex_t = ex_t + abs(number)

    for i in range(0, len(xmax)):
        if xmax[i] > image_cols:      #右下角的坐标越界，xmax > cols
            ex_r = ex_r + (xmax[i] - image_cols)
            flag = True

    for i in range(0, len(ymax)):
        if ymax[i] > image_rows:     #右下角的坐标越界，ymax > rows
            ex_b = ex_b + (ymax[i] - image_rows)
            flag = True

    if flag:
        image1 = cv2.copyMakeBorder(image, ex_t, ex_b, ex_l, ex_r, cv2.BORDER_REPLICATE)
        cv2.imwrite(os.path.join('./source_data_files/xiaocheshurentou', cc + ".jpg"), image1)

    return xmin, ymin, xmax, ymax

def main(argv=None):
    image_list()

if __name__ == '__main__':
    tf.app.run()









