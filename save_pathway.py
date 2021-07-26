#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> save_pathway
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-10 22:39
@Desc   ：用python 保存
pathway数据
=================================================='''
from utils.SavePathway import save_pathway_image,save_pathway_kgml

pathway="path:ath00460"


save_pathway_image(pathway=pathway)

save_pathway_kgml(pathway=pathway)