#! usr/bin/python
# -*- coding: utf-8 -*-
'''
@user: tianxuanWu
@project_name:数据
@file_name:app 
@date:2020/1/4
'''
import os
from flask import Flask, render_template, request
import folium
import pandas as pd
from folium import plugins
import pyecharts.options as opts
from pyecharts.charts import Line, Pie
from loguru import logger

rootPath = os.getcwd()

app = Flask(__name__)
df1 = pd.read_csv("./data/2019胡润品牌榜2.csv", encoding='utf-8', delimiter="\t", error_bad_lines=False)
df1 = df1.drop(columns=['Unnamed: 9'], axis=1)
df1[df1['Chg'] == '-'] = 0.0
df1['Chg'] = df1['Chg'].astype(float)


def plot_line(dfs):
    x_data = dfs['品牌']
    y_data = dfs['Chg']
    line = Line().set_global_opts(
                    tooltip_opts=opts.TooltipOpts(is_show=False),
                    xaxis_opts=opts.AxisOpts(type_="category"),
                    yaxis_opts=opts.AxisOpts(
                                type_="value",
                                axistick_opts=opts.AxisTickOpts(is_show=True),
                                splitline_opts=opts.SplitLineOpts(is_show=True),
                            ),
                )\
                .add_xaxis(xaxis_data=x_data)\
                .add_yaxis(series_name="Chg",
                            y_axis=y_data,
                            symbol="emptyCircle",
                            is_symbol_show=True,
                            label_opts=opts.LabelOpts(is_show=False),)

    line.render("basic_line_chart.html")
    return line.render_embed()


def china_movie_map():
    cdata = pd.read_csv('./data/movie.csv', encoding='gbk')

    latitude = 35
    longitude = 105

    china_map = folium.Map(location=[latitude, longitude], zoom_start=4)

    movies = plugins.MarkerCluster().add_to(china_map)

    for lat, lng, in zip(cdata.Y, cdata.X):
        folium.Marker(
            location=[lat, lng],
            popup='Mt. Hood Meadows',
            icon=folium.Icon(color='blue', icon='fa fa-video-camera'),
        ).add_to(movies)

    china_map.add_child(movies)
    china_map.save('./templates/china.html')


@app.route('/',methods=['GET'])
def hu_run_2019():
    regions_available = list(df1['trade'].dropna().unique())
    data_str = df1.to_html()
    return render_template('hurun.html',
                           the_res = data_str,
                           the_select_region=regions_available)

@app.route('/hurun',methods=['POST'])
def hu_run_select():
    the_region = request.form["the_region_selected"]
    regions_available = list(df1['trade'].dropna().unique())
    logger.debug(the_region)
    dfs = df1[df1['trade'] == the_region][['品牌', 'Chg']]
    dfs = dfs.reset_index(drop=True)
    data_str = dfs.to_html()
    plot_all = plot_line(dfs)
    return render_template('hurun.html',
                           the_plot_all=plot_all,
                           the_res=data_str,
                           the_select_region=regions_available,
                           )

@app.route('/movieMap', methods=['GET'])
def movie_map():
    china_movie_map()
    return render_template('china.html')


@app.route('/hurunTrade', methods=['GET'])
def hurun_trade():
    _trade = df1['trade'].value_counts()
    _trade = _trade.astype(str)
    trade = list(_trade.index)
    trade_value = list(_trade.values)
    c = (
        Pie()
            .add("", [list(z) for z in zip(trade, trade_value)], radius=["50%", "75%"])
            .set_global_opts(title_opts=opts.TitleOpts(title="2019胡润品牌榜行业分布"),
                    legend_opts=opts.LegendOpts(orient="vertical", pos_top="100%", pos_left="10%"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )

    return c.render_embed()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)