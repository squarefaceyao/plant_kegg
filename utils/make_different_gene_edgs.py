#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> make_different_gene_edgs
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-21 21:47
@Desc   ：把差异基因富集的通路转换成基因相互作用图
=================================================='''

#conding=utf8
import os
import pandas as pd
from utils.pathway2graph import pathway2graph
def main():
    '''

    Returns: 读取文件夹里全部的pathway数据，并将其转换为gene数据

    '''
    g = os.walk(r"/Users/squareface/code/different-gene/Data/pathway") # 差异分析得到的
    path_name=[]
    for path,dir_list,file_list in g:
        for file_name in file_list:
            if file_name == '.DS_Store':
                pass
            else:
                name = file_name[:-4]
            path_name.append(name)


    na={}
    for name,i in zip(path_name,range(len(path_name))):
        print(name)
        re = pathway2graph(name)
        na[i] = re
        # re.to_csv(f'./Data/all_type{name}_graph.csv',index=False)
    final = pd.concat(list(na.values()), ignore_index=True)
    print(final.shape)
    final.to_csv('../Data/different-gene-edgs.csv',index=False)


if __name__== '__main__':
    main()