# -*- coding: utf-8 -*-
import tensorflow as tf
import glob
import os
import cv2
import scipy.io as sio


picture_dir = "JPEGImages/"  # 图片的地址
label_file = "G:/Person-Re-ID/Pe-ID 项目/End-to-End 关于PRW-baseline-master/PRW-baseline-master/PRW/annotations"        #label文件的地址

def filter_label_file():   #picture_list = xxx.jpeg,......
    #处理标签文件
    file_label_list = []
    every_picture_label = []
    file_glob = os.path.join(label_file, '*.jpg' + '.mat')
    file_label_list.extend(glob.glob(file_glob))           #file_label_list为所有标签的文件列表
    for j in range(0,len(file_label_list)):
        # 得到每个标签的文件名
        label_name = []         #每个.mat的文件名,['xxxx','jpg','mat']
        aa = []
        for q in file_label_list[j].split('\\'):       # ./picture/B29T00\\20170706012121.jpeg
            aa.append(q)
        for m in aa[1].split('.'):
            label_name.append(m)

        yuan_zu = tuple(sio.loadmat(file_label_list[j]))
        for w in range(0,len(yuan_zu)):
            if yuan_zu[w] not in ['__version__','__globals__','__header__']:
                b = sio.loadmat(file_label_list[j])[yuan_zu[w]]      # 读取每个.mat文件中包含数据array的部分
                break

        # 创建.txt文件
        file_name = []
        file_name = label_name[0] + ".txt"
        '''
        for o in range(0,len(b)):
            b[o][3] = b[o][1] + b[o][3]
            b[o][4] = b[o][2] + b[o][4]
            for t in range(0,len(b[o])):
                if t == 4:
                    create_txt_file(file_name, float("{0:.4f}".format(b[o][t])), "\n")
                elif t == 0:
                    create_txt_file(file_name, int(b[o][t]), " ")
                else:
                    create_txt_file(file_name, float("{0:.4f}".format(b[o][t])), " ")
        '''
        # 调用匹配函数
        pipei_fun(picture_dir, b, file_name, label_name[0])

def create_txt_file(file_name, num, qq):
    with open(file_name, 'a') as file:
        file.write(str(num) + qq)

def pipei_fun(picture_dir, label_list, file_name, dd):

    picture = os.path.join(picture_dir+dd+".jpg")
    image = cv2.imread(picture)

    label_flag = []
    xmin = []
    ymin = []
    xmax = []
    ymax = []

    for j in range(0,len(label_list)):        #处理各个文件中的每行数据
        label_flag.append(int(label_list[j][0]))
        xmin.append(int(round(label_list[j][1])))
        ymin.append(int(round(label_list[j][2])))
        xmax.append(int(round(label_list[j][3]))+int(round(label_list[j][1])))
        ymax.append(int(round(label_list[j][4]))+int(round(label_list[j][2])))

    #扩展图片的边界,返回坐标信息
    xmin1, ymin1, xmax1, ymax1 = expand_bbox(image, xmin, ymin, xmax, ymax,dd)
    cv2.imwrite(os.path.join('./yuanshitupicture/',dd+ ".jpg"), image)

    #把更改后的坐标值写到.txt文件中去
    for i in range(0,len(xmax1)):
        create_txt_file(file_name, label_flag[i], " ")
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
        cv2.imwrite(os.path.join('./expand_picture/', cc + ".jpg"), image1)

    return xmin, ymin, xmax, ymax

def main(argv=None):
    filter_label_file()

if __name__ == '__main__':
    tf.app.run()









