#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> SavePathway
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-10 22:34
@Desc   ：
=================================================='''
from Bio.KEGG import REST
import os
from PIL import Image
from io import BytesIO


def bytes2jpg(result,img_name):
    # 将bytes结果转化为字节流
    bytes_stream = BytesIO(result)
    # 读取到图片
    roiimg = Image.open(bytes_stream)

    imgByteArr = BytesIO()  # 初始化一个空字节流
    roiimg.save(imgByteArr, format('PNG'))  # 把我们得图片以‘PNG’保存到空字节流
    imgByteArr = imgByteArr.getvalue()  # 无视指针，获取全部内容，类型由io流变成bytes。
    # dir_name = os.mkdir('baiduimg')
    with open(os.path.join('Data', img_name), 'wb') as f:
        f.write(imgByteArr)

def save_pathway_image(pathway):
    '''

    Args:
        pathway:  pathway="path:ath00460"

    Returns: save to /Data/pathway.png

    '''
    imag = REST.kegg_get(dbentries=pathway,option='image').read()
    bytes2jpg(imag,img_name=f'{pathway[5:]}.png',)
    print('save image success!!')

def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()


def save_pathway_kgml(pathway):
    '''

    Args:
        pathway: pathway="path:ath00460"

    Returns: save to /Data/pathway.xml

    '''
    kgmal = REST.kegg_get(dbentries=pathway, option='kgml').read()
    save_to_file(f'Data/{pathway[5:]}.xml', contents=kgmal)
    print('save kgml success!!')


if __name__== '__main__':
    pass