#! usr/bin/python
# -*- coding: utf-8 -*-
'''
@user: sean
@project_name:new data
@file_name:demo 
@date:2020/1/4
'''


import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Map

def map_film() -> Map:
    df = pd.read_csv('./data/movie2.csv', encoding='utf-8', delimiter="\t", error_bad_lines=False)
    df = df.drop(columns='Unnamed: 2')
    # 求pname的个数
    counts = df['pname'].value_counts()
    # print(counts)
    province = list(counts.index)
    province_values = list(counts.values)
    province_values = [str(i) for i in province_values]
    c = (
        Map()
            .add("", [list(z) for z in zip(province, province_values)], "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="全国影院分布情况"),
            visualmap_opts=opts.VisualMapOpts(max_=110),
        )
    )
    return c.render()

c = map_film()
# print(c)

# data = pd.read_csv('./data/分省人均支出.csv', encoding='gbk')
# print(data)