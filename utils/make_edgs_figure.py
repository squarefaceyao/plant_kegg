#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> make_edgs_figure
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-25 22:02
@Desc   ：读取边信息制作图片
=================================================='''
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def main():
    re = pd.read_csv('../Data/my_data-edgs.csv')

    edgs = pd.DataFrame(re, columns=['source', 'target'])

    # 作图使用的代码，节点的名字是基因
    edgs_gene = []
    for row in edgs.itertuples():
        a = [getattr(row, 'source'), getattr(row, 'target')]
        edgs_gene.append(tuple(a))

    G = nx.Graph(edgs_gene)
    plt.figure(figsize=(24, 24))
    nx.draw(G, node_color='r', with_labels=True, node_size=300)
    # plt.show()

    plt.savefig('../Figure/my_data-edgs.png', dpi=300)

if __name__ == '__main__':
    main()