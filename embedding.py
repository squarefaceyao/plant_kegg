#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> embedding
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-05 23:58
@Desc   ：把拟南芥全部的基因转换成id。用作graph制作
=================================================='''

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> embedding
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-05 23:58
@Desc   ：把拟南芥全部的基因转换成id。用作graph制作
=================================================='''


import numpy as np
import pandas as pd
import codecs
from Pathway2Graph import Pathway2Graph,gene2id,id2gene
from collections import Counter
from tensorflow.keras.preprocessing.text import Tokenizer
from keggstand.api import Kegg, NestedDictionary
import scipy.sparse as sp
import networkx as nx
import matplotlib.pyplot as plt
from torch import nn

name='ath00941'
# re = Pathway2Graph(name)
re  = pd.read_csv(f'{name}_graph.csv')

# re.columns.values

edgs = pd.DataFrame(re,columns=['source','target'])
"""
# 作图使用的代码，节点的名字是基因
edgs_gene=[]
for row in edgs.itertuples():
    a = [getattr(row, 'source'), getattr(row, 'target')]
    edgs_gene.append(tuple(a))

G = nx.Graph(edgs_gene)
plt.figure(figsize=(12,12))
nx.draw(G,node_color = 'r',with_labels=True,node_size =300)
"""

so = list(edgs['source'])
tar = list(edgs['target'])

_nodes = list(np.unique(all)) # 用unique函数获取只出现一次的元素，作为节点信息。
# 更改nodes的格式，用作id转换到基因。
nodes=[]
for i in range(len(_nodes)):
    nodes.append([_nodes[i]])


tokenizer,source_seq,target_seq = gene2id(so,tar,'ath') #  把基因转换成id
nodes_gene = id2gene(tokenizer,nodes) # 获取节点的基因信息
# so2 = id2gene(tokenizer,source_seq) # id转换成gene
# tar2 = id2gene(tokenizer,target_seq)
#
# print(so2==so) # 检查转换是否正确
# print(tar2==tar)

so2 = np.array(source_seq)
tar2 = np.array(target_seq)
all = np.hstack((so2,tar2))

edgs=[] #制作节点关系列表，节点里的每一个元素是tuple格式。
for i in range(all.shape[0]):
    edgs.append(tuple(all[i]))
    
G2 = nx.Graph(edgs)
A2 = nx.adjacency_matrix(G2)

plt.figure(figsize=(14,16))
nx.draw(G2,node_color = 'r',node_size =300)
plt.show()