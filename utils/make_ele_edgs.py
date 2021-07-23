#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> make_ele_edgs
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-21 22:55
@Desc   ：制作电信号相关的边信息
=================================================='''
import pprint
import numpy as np
import pandas as pd
import pickle
from tqdm import tqdm

def key_gene_description(key):
    '''

    Args:
        key: 根据关键字筛选基因。

    Returns:

    '''
    df = pd.read_csv('../Data/nodes_tairweb_descriptions.csv') # 爬虫获取的信息
    res = {}
    genes=[]
    for idx, data in df.iterrows():
        des = data[3]
        if key in des:
            res[data[1]] = [des]
            genes.append(data[1])
        else:
            pass
    res = pd.DataFrame(res).T
    # res.to_csv(f'./Data/ath_{key}_gene.csv')
    print(f'正在检索关键字为{key}的基因,个数为{res.shape[0]}')

    return genes

def search(keys):
    '''

    Returns: 筛选关键字列表里面的基因，并返回检索结果。

    '''
    # make_all_gene_description(organism='ath')
    res=[]
    all_res=[]

    for key in keys:

        names = key_gene_description(key)
        res.append(names)

    for re in res:
        for r in re:
            all_res.append(r)
    #
    return np.unique(all_res)  # 去除重复的元素

def main(all_res):
    '''

    Returns: 从all-gene-edgs.csv文件检索包含的节点。结果保存在../Data/ele-gene-edgs.csv

    '''
    df = pd.read_csv('../Data/all-gene-edgs.csv')
    edgs = pd.DataFrame(df, columns=['source', 'target'])

    # 遍历df每一行
    print(f'\n正在检索对应的边，需要检索的基因个数为{len(all_res)}')
    res=[]
    for name in tqdm(all_res):
        for idx, data in edgs.iterrows():
            aa = str(data)
            if name in aa:
                # 在边的信息里面检索节点，包含节点信息就返回边的数值
                value=[data[0],data[1]]
                res.append(value)
    r = np.array(res)
    print(f'共检索到{len(res)}条边')
    pd.DataFrame(r).to_csv('../Data/ele-gene-edgs.csv')

def counter(a):
    '''

    Args:
        a: 列表

    Returns: 检车列表里的重复元素

    '''
    from collections import Counter  # 引入Counter
    b = dict(Counter(a))
    # print([key for key, value in b.items() if value > 1])  # 只展示重复元素
    print(' 检查all_genes里面是否有重复元素')
    print({key: value for key, value in b.items() if value > 1})  # 展现重复元素和重复次数

if __name__ == '__main__':

    # 确定和电信号有关的关键字
    keys = ['channel', 'light', 'pump', 'Ca2+', 'eceptor',
            'K+','Cl-','H+','Na+','voltage','glutamate','transmembrane',
            'phototropin','gated','transporter','acetylcholine','jasmonic','abscisic']
    # 根据关键字搜索gene，结果保存在all_genes
    all_genes=search(keys=keys)

    print(len(all_genes))
    # 检查all_genes里面是否有重复元素
    counter(all_genes)  #  检查是否有重复的基因，
    # 从all-gene-edgs.csv文件检索包含的节点。结果保存在../Data/ele-gene-edgs.csv
    main(all_genes)

