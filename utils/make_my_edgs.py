#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> make_my_edgs
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-23 19:37
@Desc   ：制作自己需要用的edg数据,在这里需要节点里的基因名字转换成ID。
          注意： 先确定边，在制作feature
=================================================='''
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn import preprocessing
from keras_preprocessing.text import Tokenizer



# 第一步 计算对称差集
def find_edgs():
    '''

    Returns: 返回差异基因和电信号基因的对称差集的边信息

    '''

    df1=pd.read_csv('../Data/different-gene-edgs.csv') # 读取差异基因
    df2=pd.read_csv('../Data/ele-gene-edgs.csv') # 读取和电信号相关基因

    salt=list(np.unique(df1))
    ele=list(np.unique(df2))

    all_edgs = pd.concat([df1, df2], axis=0, ignore_index=True)

    intersection = [x for x in salt if x in ele]  # 列表中相同元素，可以考虑当作最终的测试集

    s = [x for x in salt if x not in ele] # 为 在s列表中而不在e列表中
    e = [y for y in ele if y not in salt] # 为 在e列表中而不在s列表中

    all_nodes=s+e
    # 寻找source和target都在all_nodes里面的边

    res=[]
    for idx, data in all_edgs.iterrows():
        if (data[0]in all_nodes):
            if (data[1]in all_nodes):
                re=[data[0],data[1]]
                res.append(re)
    r= np.array(res)
    edgs = pd.DataFrame(r, columns=['source', 'target'])

    return edgs

#  第二步 找出对称差集里面节点的标签

def extract_edgs_according_gene(edgs):
    '''

    Args:
        edgs: 对称差集里提取到的边信息

    Returns: 盐刺激 s 和电信号 e 相关基因，

    '''
    df1=pd.read_csv('../Data/different-gene-edgs.csv') # 读取差异基因
    df2=pd.read_csv('../Data/ele-gene-edgs.csv') # 读取和电信号相关基因

    salt=list(np.unique(df1))
    ele=list(np.unique(df2))

    all=np.unique(edgs)

    s = [x for x in salt if x in all]
    e = [x for x in ele if x in all]

    return s,e

def make_content_node(all_edgs,feature_num):
    '''

    Args:
        all_edgs: 差异基因和电信号基因的对称差集的边信息
        feature_num: 节点特征个数

    Returns: 保存两个文件   ../Data/my-ath.edgs   边信息
                        '../Data/my-ath.content' 节点特征信息

    '''

    #  返回节点属于哪个类别
    s,e=extract_edgs_according_gene(all_edgs)

     #  读取基因描述信息
    df=pd.read_csv('../Data/nodes_tairweb_descriptions.csv')
    df.set_index(["0"], inplace=True)

    # 提取和盐胁迫相关的基因 标签为salt (salt stress)

    label1=['salt'] * len(s)
    res1 = []
    for na1 in s:
        re1=df.loc[na1, '2']
        res1.append(re1)

    # 提取和电信号相关的基因 标签为pes (plant electrical signals)
    label2=['pes'] * len(e)
    res2 = []
    for na2 in e:
        re2=df.loc[na2, '2']
        res2.append(re2)

    # 把两部分的结果拼接在一起
    feature=res1+res2
    gene=s+e
    label=label1+label2

    # 把gene序列化

    le = preprocessing.LabelEncoder()
    le.fit(gene) # 训练gene列表字典

    e_s,e_t=[],[]
    for g in list(all_edgs['source']):
        d=le.transform([g])
        d=int(d)
        e_s.append(d)

    for g in list(all_edgs['target']):
        d=le.transform([g])
        d=int(d)
        e_t.append(d)

    # 对称差集里的边信息
    edgs=[e_s,e_t]
    final_edg=pd.DataFrame(edgs).T
    final_edg.columns=['source','target']
    final_edg.to_csv('../Data/my-ath.edgs',index=False,header=False)

    # 节点信息序列转化
    seq=[]
    for g in gene:
        d=le.transform([g])
        d=int(d)
        seq.append(d)

    # feature 编码
    tokenizer = Tokenizer(num_words=feature_num)  # 创建一个分词器，设置只考虑前1000个单词
    tokenizer.fit_on_texts(feature)  # 构建单词索引
    sequences = tokenizer.texts_to_sequences(feature)  # 将字符串转换为整数索引组成的列表
    word_index = tokenizer.word_index  # 找回单词索引
    one_hot_results = tokenizer.texts_to_matrix(feature, mode='binary')
    # 转换数据格式，后续拼接数据
    fe=one_hot_results.astype(int)
    s = np.array(seq).reshape(-1, 1)
    l = np.array(label).reshape(-1, 1)
    # 拼接数据
    final=np.hstack((s,fe,l))
    final = pd.DataFrame(final)
    # final.columns=['gene','feature','label']
    final.to_csv('../Data/my-ath.content',index=False,header=False)
    return final



def Data():
    edgs=find_edgs()
    print('边里面包含的节点个数：',len(np.unique(edgs)))
    content=make_content_node(edgs,feature_num=1600)
    return edgs, content



if __name__ == '__main__':
    Data()