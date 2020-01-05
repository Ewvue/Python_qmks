#! usr/bin/python
# -*- coding: utf-8 -*-
'''
@user: tianxuanWu
@project_name:new data
@file_name:app2 
@date:2020/1/4
'''

import os
from flask import Flask, render_template, request
import folium
import pandas as pd
from folium import plugins
import pyecharts.options as opts
from pyecharts.charts import Line, Timeline, Map
from loguru import logger

app = Flask(__name__)
# expendMap
@app.route('/', methods=['GET'])
def expend_map():
    data = pd.read_csv('./data/分省人均支出.csv', encoding='gbk')

    c = Timeline()
    for i in range(2013, 2019):
        map = (
            Map()
                .add("人均消费支出", list(zip(list(data.地区), list(data["{}".format(i)]))), "china",
                     is_map_symbol_show=False)
                .set_global_opts(
                title_opts=opts.TitleOpts(title="{}各省人均消费支出对比".format(i), subtitle="",
                                          subtitle_textstyle_opts=opts.TextStyleOpts(color="blue", font_size=18)),
                visualmap_opts=opts.VisualMapOpts(min_=6000, max_=43351, series_index=0)
            )
        )
        c.add(map, "{}".format(i))
    return c.render_embed()

@app.route('/filmMap', methods=['GET'])
def film_map():
    df = pd.read_csv('./data/movie2.csv', encoding='utf-8', delimiter="\t", error_bad_lines=False)
    df = df.drop(columns='Unnamed: 2')
    # 求pname的个数
    counts = df['pname'].value_counts()
    # print(counts)
    counts = counts.astype(str)
    province = list(counts.index)
    province_values = list(counts.values)
    map = (
        Map()
            .add("全国影院分布", list(zip(province, province_values)), "china", is_map_symbol_show=False)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="全国影院分布情况", subtitle="",
                                      subtitle_textstyle_opts=opts.TextStyleOpts(color="blue", font_size=18)),
            visualmap_opts=opts.VisualMapOpts(min_=0, max_=110, series_index=0),
        )
    )
    return map.render_embed()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=4000, debug=True)