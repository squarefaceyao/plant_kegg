#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> request_tair
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-19 16:45
@Desc   ：获取TAIR网站里基因描述信息
=================================================='''
import requests
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import re

def crawler_tair(gene):
    # genes=pd.rad
    kaitou='https://www.arabidopsis.org/servlets/TairObject?type=locus&name='
    # gene='AT1G04310'
    url=kaitou+gene
    page=urllib.request.urlopen(url)

    soup = BeautifulSoup(page,'html.parser')

    symbol=soup.select('.sm td')[0].get_text()
    # print('Description',soup.select('tr td'))
    des=[]
    # print('循环迭代所有ul下面的所有li节点的文本值')

    for li in soup.select('tr td'):
        des.append(li.text)

    description=des[11]
    return symbol, description





if __name__ =='__main__':

    genes=pd.read_csv('../Data/all_pathway_gene_des.csv')['0']
    res={}
    i=1
    for gene in genes:
        print(f'这是第{i}个： ',gene)
        symbol, description = crawler_tair(gene=gene)
        res[gene] = [gene, symbol, description]
        # print(description)
        i=i+1



    pd.DataFrame(res).T.to_csv('../Data/test.csv')

