import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import plotly.express as px

# 引用aqua.css
external_stylesheets = ['https://cdn.jsdelivr.net/gh/alphardex/aqua.css/dist/aqua.min.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

path = r"./lab3-datasets/google-play-store-apps/googleplaystore.csv"
df = pd.read_csv(path, encoding='ANSI')

# 获取某一列的唯一分类
categories = df['Category'].unique()
types = ['Free', 'Paid']
content_rates = df['Content Rating'].unique()

app.layout = html.Div([

    # content-rating 饼状图
    html.Div([
        dcc.Graph(
            id='content-rating-graph',
            animate=False),
    ],
        style={'width': '50%', 'margin-left': '20%'}),

    # 选择软件种类
    html.Div([
        html.Div([
            dcc.Dropdown(
                id="Category",
                options=[{'label': i, 'value': i} for i in categories],
                value='ART_AND_DESIGN'
            )],
            style={'width': '20%', 'display': 'inline-block', 'padding': '10px 20px', 'margin-left': '25%'}),

        # 选择软件付费类型
        html.Div([
            dcc.Dropdown(
                id="Type",
                options=[{'label': i, 'value': i} for i in types],
                value='Free'
            )],
            style={'width': '20%', 'display': 'inline-block', 'padding': '10px 20px', 'margin-right': '25%'}), ]),

    # content-rating 内容分级的单选盒子
    html.Div([
        dcc.RadioItems(
            id='content-rating-radio',
            options=[
                {'label': i, 'value': i} for i in content_rates
            ],
            value='Everyone',
            labelStyle={'padding': '0 20px', 'display': 'inline-block'}
        )
    ],
        style={'padding': '10px 50px', 'margin': '0 auto', 'margin-left': '30%', 'margin-top': '50px'}),
    # installs-genres 柱状图
    html.Div([
        dcc.Graph(
            id='installs-genres',
            animate=True
        )],
        style={'width': '80%', 'display': 'inline-block', 'margin-top': '40px', 'margin-left': '10%',
               'padding': '10px 20px'}),

    # reviews-installs散点图 和 installs-size折线图 和 installs-rating柱状图
    html.Div([

        html.Div([
            dcc.Graph(
                id='reviews-installs',
                animate=True
            ),
        ],
            style={'width': '30%', 'margin-top': '40px', 'display': 'inline-block', 'margin-left': '5%'}
        ),

        html.Div([
            dcc.Graph(
                id='installs-size',
                animate=True
            ),
        ],
            style={'width': '30%', 'margin-top': '40px', 'display': 'inline-block'}
        ),
        html.Div([
            dcc.Graph(
                id='installs-rating',
                animate=True
            ), ],
            style={'width': '30%', 'margin-top': '40px', 'display': 'inline-block'}),

    ]),

])


# content-rating饼状图
# 回调函数，当category或type发生变化时调动
@app.callback(
    dash.dependencies.Output('content-rating-graph', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
    ]
)
def update_pie_chart(category_value, type_value):
    # 根据选定的category和type筛选数据
    filtered_df = df[(df['Category'] == category_value) & (df['Type'] == type_value)]

    # 提取筛选后数据集中的Content Rating
    content_rating_list = list(filtered_df['Content Rating'])
    content_rating_values = [0] * len(content_rating_list)
    for _, row in filtered_df.iterrows():
        content_rating = row['Content Rating']
        # 取第一个出现该类型数据的索引作为计数的index
        content_rating_index = content_rating_list.index(content_rating)
        content_rating_values[content_rating_index] += 1
    data = [
        go.Pie(
            labels=content_rating_list,
            values=content_rating_values
        )
    ]

    layout = go.Layout(
        margin={'l': 130, 'b': 30, 't': 50, 'r': 0},
        height=300,
        hovermode='closest'
    )

    return {'data': data, 'layout': layout}


# installs-size 折线图，反映大小对下载量的影响
@app.callback(
    dash.dependencies.Output('installs-size', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('content-rating-radio', 'value')
    ]
)
def update_installs_size_series(category_value, type_value, radio_value):
    # 根据选定的category、type和radio筛选数据
    filtered_df = df[
        (df['Category'] == category_value) & (df['Content Rating'] == radio_value) & (df['Type'] == type_value)]

    sizes = [
        '0~300k', '300k~600k', '600k~900k', '900k~25m', '25m~50m',
        '50m~75m', '75m~100m', 'Varies with device'
    ]
    # 初始化安装数量列表，初始值为0
    installs = [0] * len(sizes)

    for _, row in filtered_df.iterrows():
        size = row['Size']
        # 获取当前行的Installs并去除逗号
        installs_str = row['Installs'].split('+')[0].replace(',', '')
        installs_int = int(installs_str)

        if size == 'Varies with device':
            installs[-1] += installs_int
        elif size[-1] == 'k':
            i = int(float(size[:-1]) // 300)
            installs[i] += installs_int
        else:
            i = int(float(size[:-1]) // 25) + 3
            installs[i] += installs_int

    data = [
        {
            'x': sizes,
            'y': installs,
            'mode': 'lines+markers',
            'type': 'scatter',
            'name': 'Line'
        }
    ]

    layout = go.Layout(
        xaxis={'title': 'Size'},
        yaxis={'title': 'Installs'},
        title='Installs-Size',

        margin={'l': 130, 'b': 100, 't': 50, 'r': 40},
        height=500,
        hovermode='closest'
    )

    return {'data': data, 'layout': layout}


# 封装好的绘制散点图函数
def create_scatter_plot(x_values, x_title, y_values, y_title, text, title):
    scatter_data = go.Scatter(
        x=x_values,
        y=y_values,
        text=text,
        mode='markers',
        marker={
            'size': 15,
            'opacity': 0.5,
            'line': {
                'width': 0.5,
                'color': 'white'
            }
        }
    )

    layout = go.Layout(
        xaxis={'title': x_title},
        yaxis={'title': y_title},
        title=title,
        margin={'l': 130, 'b': 100, 't': 50, 'r': 40},
        height=500,
        hovermode='closest'
    )

    return {'data': [scatter_data], 'layout': layout}


# installs-size 散点图，反映评论和安装数的关系
@app.callback(
    dash.dependencies.Output('reviews-installs', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('content-rating-radio', 'value')
    ]
)
def update_reviews_installs_scatter(category_value, type_value, rating):
    filtered_df = df[(df['Category'] == category_value) & (df['Type'] == type_value) & (df['Content Rating'] == rating)]

    reviews = filtered_df['Reviews']
    installs = filtered_df['Installs']
    names = filtered_df['App']

    return create_scatter_plot(installs, 'Installs', reviews, 'Reviews', names, 'Reviews-Installs')


# 绘制柱状图
def create_bar_plot(x_values, x_title, y_values, y_title, title, height_value, bt_margin):
    bar_data = go.Bar(
        x=x_values,
        y=y_values,
    )

    layout = go.Layout(
        xaxis={'title': x_title},
        yaxis={'title': y_title},
        title=title,
        margin={'l': 130, 'b': bt_margin, 't': 50, 'r': 40},
        height=height_value,
        hovermode='closest'
    )

    return {'data': [bar_data], 'layout': layout}


# installs-rating柱状图
@app.callback(
    dash.dependencies.Output('installs-rating', 'figure'),
    [
        dash.dependencies.Input('Category', 'value'),
        dash.dependencies.Input('Type', 'value'),
        dash.dependencies.Input('content-rating-radio', 'value')
    ]
)
def update_installs_rating_bar(category_value, type_value, rating):
    filtered_df = df[(df['Category'] == category_value) & (df['Type'] == type_value) & (df['Content Rating'] == rating)]

    installs = [0] * 8
    ratings = ['1~1.5', '1.5~2', '2~2.5', '2.5~3', '3~3.5', '3.5~4', '4~4.5', '4.5~5']
    rating_ranges = [1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]

    for _, row in filtered_df.iterrows():
        if not np.isnan(row['Rating']):
            installs_str = row['Installs'].split('+')[0].replace(',', '')
            installs_int = int(installs_str)
            rating = float(row['Rating'])
            for i in range(len(rating_ranges) - 1):
                if rating_ranges[i] <= rating < rating_ranges[i + 1]:
                    installs[i] += installs_int
                    break
            else:
                installs[-1] += installs_int

    return create_bar_plot(ratings, 'Rating', installs, 'Installs', 'Installs-Rating', 500, 100)


# installs-category 柱状图
@app.callback(
    dash.dependencies.Output('installs-genres', 'figure'),
    [
        dash.dependencies.Input('content-rating-radio', 'value')
    ]
)
def update_installs_category_scatters(radio):
    filtered_df = df[(df['Content Rating'] == radio)]

    installs = []
    genres = df['Genres'].unique()
    for i in genres:
        installs.append(0)
    for _, row in filtered_df.iterrows():
        installs_str = row['Installs'].split('+')[0].replace(',', '')
        installs_int = int(installs_str)
        installs[np.where(genres == row['Genres'])[0][0]] += installs_int

    return create_bar_plot(genres, 'Genres', installs, 'Installs', 'Installs-Genres', 400, 200)


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')
