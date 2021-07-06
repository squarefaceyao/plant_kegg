#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> Pathway2Graph
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-05 18:43
@Desc   ：根据pathway的名字，生成图信息，选择的节点类别都是基因。
=================================================='''

from keggstand.api import Kegg, NestedDictionary
import numpy as np
import pandas as pd
import codecs
from tensorflow.keras.preprocessing.text import Tokenizer


def Pathway2Graph(name):
    '''

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

def gene2id(source,target,organism):
    '''
    source: source基因列表
    target： target基因列表
    organism: 物种的缩写
    Returns: 把基因转换成id

    '''
    all_gene = pd.read_csv(f'./kegg_all_gene_{organism}.csv')
    # all_gene = all_gene.columns = ['gene']

    gene_name = list(all_gene['gene'])
    # gene_name = all_gene['gene'].values.tolist()
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(gene_name)

    source_seq = tokenizer.texts_to_sequences(source)
    target_seq = tokenizer.texts_to_sequences(target)


    return tokenizer,source_seq,target_seq

def id2gene(tokenizer,sequence):
    '''
    sequence格式：list = [[id1],[id2],[id3],]

    Args:
        tokenizer: 训练好的tokenizer
        sequence: 转换成id的基因序列

    Returns: id对应的基因名字

    '''
    seq2so = tokenizer.sequences_to_texts(sequence)
    seq2so = [item.upper() for item in seq2so]

    return seq2so


def make_all_gene(organism):
    '''

    Args:
        organism: 物种的缩写，拟南芥：ath

    Returns:

    '''
    client = Kegg(cache=True)
    accessions = client.list_genes(organism=organism)
    all_gene = []
    for i in range(len(accessions)):
        a = accessions[i][0][4:]
        all_gene.append(a)

    all_gene = pd.DataFrame(np.array(all_gene))
    all_gene.columns = ['gene']
    all_gene.to_csv(f'kegg_all_gene_{organism}.csv',index=False)

    return "保存成功"


# make_all_gene(organism='ath')

#
# name='ath00941'
# re = Pathway2Graph(name)

# re.to_csv(f'./{name}_graph.csv',index=False)

