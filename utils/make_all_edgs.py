#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> make_all_edgs
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-21 21:41
@Desc   ：获取全部拟南芥的边信息，gene-gene
=================================================='''

from keggstand.api import Kegg, NestedDictionary
import numpy as np
import pandas as pd
from utils.pathway2graph import pathway2graph
from tqdm import tqdm

def main():
    '''

    Returns:

    '''
    client = Kegg(cache=True)
    accessions = client.list_pathways(organism='ath')
    path_name = []
    for i in range(len(accessions)):
        a = accessions[i][0][5:]
        path_name.append(a)

    na={}
    for name,i in zip(path_name,range(len(path_name))):
        re = pathway2graph(name)
        na[i] = re
        # re.to_csv(f'./Data/all_type{name}_graph.csv',index=False)
    final = pd.concat(list(na.values()), ignore_index=True)
    print(final.shape)
    final.to_csv('../Data/all-gene-edgs.csv',index=False)



if __name__ == '__main__':
    main()

