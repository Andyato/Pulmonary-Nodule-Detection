"""conver to xml"""
import copy
from lxml.etree import Element, SubElement, tostring, ElementTree
import cv2
import os

template_file = 'sample.xml'
target_dir = './data/nodules/Annotations/'
image_dir = './data/nodules/JPEGImages/'  
train_file = './data/nodules/annotation/bbox.txt'  

if not os.path.exists(target_dir):
    os.makedirs(target_dir)

with open(train_file) as f:
    trainfiles = f.readlines()  # (filename label x_min y_min x_max y_max)

file_names = []

for line in trainfiles:
    trainFile = line.split(',')
    file_name = trainFile[0].split('/')[-1]
    print(file_name)

    if file_name not in file_names:
        file_names.append(file_name)
        lable = trainFile[1]
        xmin = trainFile[2]
        ymin = trainFile[3]
        xmax = trainFile[4]
        ymax = trainFile[5]

        tree = ElementTree()
        tree.parse(template_file)
        root = tree.getroot()

        # filename
        root.find('filename').text = file_name

        # size
        sz = root.find('size')
        im = cv2.imread(image_dir + file_name)
        sz.find('height').text = str(im.shape[0])
        sz.find('width').text = str(im.shape[1])
        sz.find('depth').text = str(im.shape[2])

        # object 
        obj = root.find('object')

        obj.find('name').text = lable
        bb = obj.find('bndbox')
        bb.find('xmin').text = xmin
        bb.find('ymin').text = ymin
        bb.find('xmax').text = xmax
        bb.find('ymax').text = ymax

    else:
        lable = trainFile[1]
        xmin = trainFile[2]
        ymin = trainFile[3]
        xmax = trainFile[4]
        ymax = trainFile[5]

        obj_ori = root.find('object')

        obj = copy.deepcopy(obj_ori)  

        obj.find('name').text = lable
        bb = obj.find('bndbox')
        bb.find('xmin').text = xmin
        bb.find('ymin').text = ymin
        bb.find('xmax').text = xmax
        bb.find('ymax').text = ymax
        root.append(obj)

    xml_file = file_name.replace('png', 'xml')

    tree.write(target_dir + xml_file, encoding='utf-8')