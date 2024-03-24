# -- coding: utf-8 --
from pyecharts.charts import Map
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.faker import Faker
import pandas as pd
import webbrowser
import cv2
df = pd.read_csv('cu2022.csv', encoding='gbk')
df.head()
df.describe()
df.isnull().sum()
df['升/降'].fillna(0, inplace=True)
df.isnull().sum()
df.fillna(0, inplace=True)
df.describe()
g = df.groupby('省市')
# 各省份大学数量
df_counts = g.count()['排名']
df0 = df_counts.copy()
df0.sort_values(ascending=False, inplace=True)
df_means0 = g.mean()['总分']
df_means = df_means0.round(2)
df1 = pd.concat([df_counts, df_means], join='outer', axis=1)
df1.columns = ['数量', '平均分']
df1.sort_values(by=['平均分'], ascending=False, inplace=True)
df1.sort_values(by=['平均分'], inplace=True)
d1 = df1.index.tolist()
d2 = df1['数量'].values.tolist()
d3 = df1['平均分'].values.tolist()
bar = (
    Bar()
    .add_xaxis(d1)
    .add_yaxis('数量', d2)
    .add_yaxis('平均分数', d3)
    .reversal_axis()
    .set_series_opts(label_opts=opts.LabelOpts(position='right'))
    .set_global_opts(
        title_opts=opts.TitleOpts(title='中国大学排名'),
        yaxis_opts=opts.AxisOpts(name='省份'),
        xaxis_opts=opts.AxisOpts(name='量'),
    )
)
bar.render_notebook()
bar.render('bar.html')
webbrowser.open('bar.html')
name = df_counts.index.tolist()
count = df_counts.values.tolist()
c = (
    Pie()
    .add(
        '',
        [list(z) for z in zip(name, count)],
        radius=['20%', '60%'],
        center=['50%', '65%'],
        rosetype="radius",
        label_opts=opts.LabelOpts(is_show=False),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter='{b}: {c}'))
)
c.render_notebook()
c.render('c.html')
webbrowser.open('c.html')
name = df0.index.tolist()
count = [int(value) for value in df0.values.tolist()]
m = (
        Map()
        .add('', [list(z) for z in zip(name, count)], 'china')
        .set_global_opts(
            title_opts=opts.TitleOpts(title='中国大学排名'),
            visualmap_opts=opts.VisualMapOpts(max_=40, split_number=8, is_piecewise=True),
        )
    )
m.render_notebook()
m.render('m.html')
webbrowser.open('m.html')