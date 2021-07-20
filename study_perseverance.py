#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''=================================================
@Project -> File   ：plant-kegg -> test_perseverance
@IDE    ：PyCharm
@Author ：Mr. Y
@Date   ：2021-07-19 23:51
@Desc   ：
=================================================='''
from utils.perseverance import Perseverance
import torch

dataset = Perseverance(root='/tmp/Cora', name='Cora')
device = torch.device('cuda')

data = dataset[0].to(device)
