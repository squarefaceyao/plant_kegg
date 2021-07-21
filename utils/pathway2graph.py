#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> pathway2graph
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-21 21:50
@Desc   ：
            pathway数据转换成图
=================================================='''
from keggstand.api import Kegg
import numpy as np
import pandas as pd

def pathway2graph(name):
    '''
    对网络环境有要求
    Args:
        name: payhway的名字

    Returns: source 和target基因的名字

    '''

    client = Kegg(cache=True)
    pathway = client.get_pathway(pathway=f'path:{name}')

    node=pathway.entries
    edgs = pathway.relations

    target,tar_type=[],[]
    source,sour_type=[],[]

    for i in range(0,len(edgs)):
        # entry_type 只有两种类型 gene 和map
        if edgs[i].target.entry_type == 'gene' and edgs[i].source.entry_type=='gene' :
            target.append(edgs[i].target.accessions[0][4:])
            tar_type.append(edgs[i].target.entry_type)
            source.append(edgs[i].source.accessions[0][4:])
            sour_type.append(edgs[i].source.entry_type)
    tar = np.array(target)
    tar_type = np.array(tar_type)
    sour = np.array(source)
    sour_type = np.array(sour_type)

    re = pd.DataFrame(np.vstack((sour, sour_type, tar, tar_type))).T
    re.columns = ['source','source_type','target','target_type']
    return re

if __name__ == '__main__':
    pass