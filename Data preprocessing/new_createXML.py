# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import cv2
from itertools import islice
from xml.dom.minidom import Document
import tensorflow as tf
import glob
import os
from PIL import Image

imgpath = 'JPEGImages/'
xmlpath_new = 'Annota/'
foldername = 'VOC2012'


picture_dir = "./source_data_files/Yinlu_and_Quecao_file/img"                         # 图片的地址
label_file = "./source_data_files/Yinlu_and_Quecao_file/images_list_fix.label"    #label文件的地址

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


    dd = []
    cc = []
    #处理标签文件
    with open(label_file, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()     #整行读取数据
            if not lines:
                break

            #提取出标签中的图片行,lines = mmexport1500952078673.jpg
            if lines[0] == 'i':    #图片的路径信息
                name = []  # 类别的名
                labels = []  # 类别的标签信息
                dd = []
                cc = []
                aa = []
                for k in lines.split('/'):
                    aa.append(k)
                for i in aa[1].split('\n'):
                    dd.append(i)                #dd[0] = 'B29T00_20170706012121.jpeg'
                for j in dd[0].split('.'):
                    cc.append(j)                #cc[0] = 'B29T00 20170706012121'
                continue

            #处理数字行
            if int(len(lines)) >= 2 and int(len(lines) <= 3):
                num = int(lines)
                if num == 0:
                    continue
                else:
                    label_list = []
                    #处理图片标签位置信息
                    for i in range(0, num):
                        lines = file_to_read.readline()
                        if not lines:
                            break
                        else:
                            #分割标签和标签名字，以空格的形式
                            temp = []
                            mm = []
                            for x in lines.split(' '):
                                temp.append(x)                #temp[0]='22,33,44,55' ; temp[1] = 'y_h_yellow\n'
                            for y in temp[1].split('\n'):
                                mm.append(y)                  #mm[0] = 'y_h_yellow'

                            name.append(mm[0])
                            labels.append(temp[0])

                    # 保存图片到某个文件中去，统一后缀.jpg格式
                    picture = os.path.join(picture_dir, dd[0])
                    image = cv2.imread(picture)
                    cv2.imwrite(os.path.join('./JPEGImages', cc[0] + ".jpg"), image)

                    picture_jpg = os.path.join(cc[0]+".jpg")
                    create(name, labels, picture_jpg, cc[0])     #调用创建.XML文件


def insertObject(doc, datas, name1):
    obj = doc.createElement('object')
    name = doc.createElement('name')
    #name.appendChild(doc.createTextNode(datas[0]))
    name.appendChild(doc.createTextNode(name1))
    obj.appendChild(name)

    pose = doc.createElement('pose')
    pose.appendChild(doc.createTextNode('Unspecified'))
    obj.appendChild(pose)

    truncated = doc.createElement('truncated')
    truncated.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(truncated)

    difficult = doc.createElement('difficult')
    difficult.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(difficult)

    bndbox = doc.createElement('bndbox')
    xmin = doc.createElement('xmin')
    xmin.appendChild(doc.createTextNode(str(datas[0])))
    bndbox.appendChild(xmin)

    ymin = doc.createElement('ymin')
    ymin.appendChild(doc.createTextNode(str(datas[1])))
    bndbox.appendChild(ymin)

    xmax = doc.createElement('xmax')
    xmax.appendChild(doc.createTextNode(str(datas[2])))
    bndbox.appendChild(xmax)

    ymax = doc.createElement('ymax')
    if '\r' == str(datas[3])[-1] or '\n' == str(datas[3])[-1]:
        data = str(datas[3])[0:-1]
    else:
        data = str(datas[3])
    ymax.appendChild(doc.createTextNode(data))
    bndbox.appendChild(ymax)

    obj.appendChild(bndbox)
    return obj


def create(name1, labels, pictureName, xmlName):
    if 0 == len(name1):
        print('bounding box information error')
    else:
        imageFile = imgpath + pictureName      #通过具体的地址来加载图片
        img = cv2.imread(imageFile)
        imgSize = img.shape

        xmlName = os.path.join(xmlName+'.xml')
        f = open(xmlpath_new + xmlName, "w")
        doc = Document()
        annotation = doc.createElement('annotation')
        doc.appendChild(annotation)

        folder = doc.createElement('folder')
        folder.appendChild(doc.createTextNode(foldername))
        annotation.appendChild(folder)

        filename = doc.createElement('filename')
        filename.appendChild(doc.createTextNode(pictureName))
        annotation.appendChild(filename)

        source = doc.createElement('source')
        database = doc.createElement('database')
        database.appendChild(doc.createTextNode('The VOC2007 Database'))
        source.appendChild(database)
        source_annotation = doc.createElement('annotation')
        source_annotation.appendChild(doc.createTextNode('PASCAL VOC2007'))
        source.appendChild(source_annotation)
        image = doc.createElement('image')
        image.appendChild(doc.createTextNode('flickr'))
        source.appendChild(image)
        flickrid = doc.createElement('flickrid')
        flickrid.appendChild(doc.createTextNode('NULL'))
        source.appendChild(flickrid)
        annotation.appendChild(source)

        owner = doc.createElement('owner')
        flickrid = doc.createElement('flickrid')
        flickrid.appendChild(doc.createTextNode('NULL'))
        owner.appendChild(flickrid)
        name = doc.createElement('name')
        name.appendChild(doc.createTextNode('idaneel'))
        owner.appendChild(name)
        annotation.appendChild(owner)

        size = doc.createElement('size')
        width = doc.createElement('width')
        width.appendChild(doc.createTextNode(str(imgSize[1])))
        size.appendChild(width)
        height = doc.createElement('height')
        height.appendChild(doc.createTextNode(str(imgSize[0])))
        size.appendChild(height)
        depth = doc.createElement('depth')
        depth.appendChild(doc.createTextNode(str(imgSize[2])))
        size.appendChild(depth)
        annotation.appendChild(size)

        segmented = doc.createElement('segmented')
        segmented.appendChild(doc.createTextNode(str(0)))
        annotation.appendChild(segmented)

        #插入目标的信息,即object信息
        for i in range(0,len(name1)):
            datas = []
            for j in labels[i].split(','):
                datas.append(j)              #datas=['11','22','33','44']

            #简单处理图片越界，小于0的值全部赋值为0，超出的部分全部等于边界
            #读取图片的宽高值
            if int(datas[0]) < 0:
                datas[0] = str(0)
            if int(datas[1]) < 0:
                datas[1] = str(0)
            if int(datas[2]) > imgSize[1]:
                datas[2] = str(imgSize[1])
            if int(datas[3]) > imgSize[0]:
                datas[3] = str(imgSize[0])

            annotation.appendChild(insertObject(doc, datas, name1[i]))
    try:
        f.write(doc.toprettyxml(indent='    '))
        f.close()
    except:
        pass


if __name__ == '__main__':
    image_list()