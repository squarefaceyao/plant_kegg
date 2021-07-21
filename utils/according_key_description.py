#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> according_key_description
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-21 18:46
@Desc   ：根据关键字，检索基因表述信息
=================================================='''
import pandas as pd

def according_key_description(key):
    '''

    Args:
        key: 根据关键字筛选基因。

    Returns:

    '''
    df = pd.read_csv('../Data/nodes_tairweb_descriptions.csv')
    res = {}
    for idx, data in df.iterrows():
        des = data[3]
        if key in des:
            res[data[1]] = [des]
        else:
            pass
    res = pd.DataFrame(res).T
    # res.to_csv(f'./Data/ath_{key}_gene.csv')
    name = list(res.index)
    # print(res.shape)
    return name

def main():
    res={}
    keys = ['channel', 'light', 'pump', 'Ca2+', 'receptor']
    for key in keys:
        names = according_key_description(key)
        res[key]=names
    print(res)

if __name__ == '__main__':
    main()


