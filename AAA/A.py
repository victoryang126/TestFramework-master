import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import mpld3
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

def plot_waveform_from_csv(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)
    print(df.columns)
    # 绘制图表
    plt.figure(figsize=(10, 6))

    # 根据需要绘制不同参数的曲线
    plt.plot(df['Time[s]'], df['ENS'], label='ENS')
    plt.plot(df['Time[s]'], df['Trigger'], label='Trigger')
    plt.plot(df['Time[s]'], df['IGN'], label='IGN')
    plt.plot(df['Time[s]'], df['SAFING'], label='SAFING')

    # 添加图例、标签等
    plt.legend()
    plt.xlabel('Time (seconds)')
    plt.ylabel('Parameter Value')
    plt.title('Analysis of Waveform Parameters')
    plt.grid(True)

    # 显示图表
    plt.show()

def analyze_ens_data(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 计算当前采样点到下一个采样点的间隔时间
    durations = df['Time[s]'].diff().fillna(0)

    # 创建DataFrame保存结果
    result_df = pd.DataFrame({'ENS_Value': df['ENS'], 'Duration': durations.shift(-1).fillna(0)})

    return result_df


def plot_square_wave_from_csv(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 绘制方波图表
    plt.figure(figsize=(10, 6))

    # 根据需要绘制不同参数的方波曲线
    plt.step(df['Time[s]'], df['ENS'], label='ENS')
    plt.step(df['Time[s]'], df['Trigger'], label='Trigger')
    plt.step(df['Time[s]'], df['IGN'], label='IGN')
    plt.step(df['Time[s]'], df['SAFING'], label='SAFING')

    # 添加图例、标签等
    plt.legend()
    plt.xlabel('Time (seconds)')
    plt.ylabel('Parameter Value')
    plt.title('Analysis of Square Waveform Parameters')
    plt.grid(True)

    # 显示图表
    plt.show()

def plot_binary_square_wave_from_csv(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 绘制二值方波图表
    plt.figure(figsize=(10, 6))

    # 根据需要绘制不同参数的二值方波曲线
    plt.step(df['Time[s]'], df['ENS'], where='post', label='ENS')
    plt.step(df['Time[s]'], df['Trigger'], where='post', label='Trigger')
    plt.step(df['Time[s]'], df['IGN'], where='post', label='IGN')
    plt.step(df['Time[s]'], df['SAFING'], where='post', label='SAFING')

    # 设置Y轴仅显示0和1
    plt.yticks([0, 1])

    # 添加图例、标签等
    plt.legend()
    plt.xlabel('Time (seconds)')
    plt.ylabel('Parameter Value')
    plt.title('Binary Square Waveform Parameters')
    plt.grid(True)

    # 显示图表
    plt.show()




def plot_interactive_square_wave_from_csv(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 创建交互式图表
    fig = go.Figure()

    # 添加二值方波图形
    for column in ['ENS', 'Trigger', 'IGN', 'SAFING']:
        fig.add_trace(go.Scatter(
            x=df['Time[s]'],
            y=df[column],
            mode='lines+markers',
            name=column,
            line=dict(shape='hv'),  # 设置线段形状为水平和垂直
        ))

    # 设置布局
    fig.update_layout(
        title='Interactive Binary Square Waveform Parameters',
        xaxis=dict(title='Time (seconds)'),
        yaxis=dict(title='Parameter Value', tickvals=[0, 1], range=[-0.1, 1.1]),
        legend=dict(x=0, y=1),
        hovermode='x unified',
        modeBarButtonsToRemove=['toImage'],
    )

    # 显示交互式图表
    fig.show()

    fig.write_html("table.html")
    html_code = fig.to_html(full_html=False, include_plotlyjs=False, include_mathjax=False)
    print(html_code)
# 用法示例：传入CSV文件路径

def plot_interactive_square_wave_from_csv2(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 获取ENS列的最大值
    max_ens_value = df['ENS'].max()

    # 创建交互式图表
    fig = go.Figure()

    # 添加二值方波图形
    for column in ['ENS', 'Trigger', 'IGN', 'SAFING']:
        fig.add_trace(go.Scatter(
            x=df['Time[s]'],
            y=df[column],
            mode='lines+markers',
            name=column,
            line=dict(shape='hv'),  # 设置线段形状为水平和垂直
        ))

    # 设置布局
    fig.update_layout(
        title='Interactive Binary Square Waveform Parameters',
        xaxis=dict(title='Time (seconds)'),
        yaxis=dict(title='Parameter Value', tickvals=[i  for i in range(0,max_ens_value)], range=[0, max_ens_value]),
        legend=dict(x=0, y=1),
        hovermode='x unified'
    )

    # 显示交互式图表
    fig.show()

    fig.write_html("table.html")
    html_code = fig.to_html(full_html=False)
    print(html_code)

def analyze_ens_data_to_df(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 获取ENS列的数值和时间间隔
    ens_values = df['ENS'].tolist()
    time_intervals = [df['Time[s]'][i + 1] - df['Time[s]'][i] for i in range(len(df['Time[s]']) - 1)]

    # 获取当前采样点和下一个不同值的采样点的时间间隔
    sample_points = []
    sample_times = []

    current_value = ens_values[0]
    current_time = 0.0

    for value, time_interval in zip(ens_values[1:], time_intervals):
        if value != current_value:
            sample_points.append(current_value)
            sample_times.append(current_time + time_interval)  # 更新为当前时间间隔加上下一个不同值的时间间隔

            current_value = value
            current_time = 0.0
        else:
            current_time += time_interval

    # 添加最后一个采样点
    sample_points.append(current_value)
    sample_times.append(current_time)

    # 构建结果DataFrame
    result_df = pd.DataFrame({
        'Sample Points': sample_points,
        'Sample Times': sample_times
    })

    return result_df

def analyze_ens_data_to_df3(file_path):
    # 从CSV文件加载数据到DataFrame
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 找到ENS列中当前采样点和下一个不同值的采样点的索引
    # df['ENS']：获取 DataFrame 中名为 'ENS' 的列。
    # .shift()：将该列向下平移一行，即将每个元素替换为其下一行的值。
    # .ne()：执行逻辑运算，返回一个布尔值 Series，指示两列中的元素是否不相等。
    # 因此，df['ENS'].ne(df['ENS'].shift()) 返回一个布尔值 Series，其中每个元素表示当前行与下一行是否具有不同的 'ENS' 列值。在你的上下文中，它被用于找到 'ENS' 列中当前采样点和下    #一个不同值的采样点的索引。
    change_indices = df['ENS'].diff().ne(0)
    print(change_indices)

    # 获取当前采样点和下一个不同值的采样点的时间间隔和采样点值
    sample_times = df.loc[change_indices, 'Time[s]'].diff().fillna(0).tolist()
    sample_points = df.loc[change_indices, 'ENS'].tolist()

    # 构建结果DataFrame
    result_df = pd.DataFrame({
        'Sample Points': sample_points,
        'Sample Times': sample_times
    })

    return result_df



def analyze_ens_data_to_df4(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 找到ENS列中当前采样点和下一个不同值的采样点的索引
    change_indices = df['ENS'].ne(df['ENS'].shift())

    # 获取当前采样点到下一个不同值的采样点的时间间隔和采样点值
    sample_times = df['Time[s]'][change_indices].diff().fillna(0).tolist()
    sample_points = df['ENS'][change_indices].tolist()

    # 构建结果DataFrame
    result_df = pd.DataFrame({
        'Sample Points': sample_points,
        'Sample Times': sample_times
    })

    return result_df


def analyze_ens_data_to_df5(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 找到ENS列中当前采样点和下一个不同值的采样点的索引
    change_indices = df['ENS'].ne(df['ENS'].shift())
    print(change_indices)
    print(df['Time[s]'][change_indices])
    # 获取当前采样点和下一个不同值的采样点之间的时间间隔和采样点值
    sample_times = df['Time[s]'][change_indices].diff().shift(-1).fillna(0).tolist()
    sample_points = df['ENS'][change_indices].tolist()

    # 构建结果DataFrame
    result_df = pd.DataFrame({
        'Sample Points': sample_points,
        'Sample Times': sample_times
    })

    return result_df

def plot_waveform_from_csv_to_html(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 绘制图表
    plt.figure(figsize=(10, 6))

    # 根据需要绘制不同参数的曲线
    plt.plot(df['Time[s]'], df['ENS'], label='ENS')
    plt.plot(df['Time[s]'], df['Trigger'], label='Trigger')
    plt.plot(df['Time[s]'], df['IGN'], label='IGN')
    plt.plot(df['Time[s]'], df['SAFING'], label='SAFING')

    # 添加图例、标签等
    plt.legend()
    plt.xlabel('Time (seconds)')
    plt.ylabel('Parameter Value')
    plt.title('Analysis of Waveform Parameters')
    plt.grid(True)

    # 将Matplotlib图形转换为HTML
    html_fig = mpld3.fig_to_html(plt.gcf())

    # 保存为HTML文件
    with open("output.html", "w") as html_file:
        html_file.write(html_fig)

    # 显示图表（可选）
    mpld3.show()

def plot_waveform_from_csv_to_html_code_bokeh(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 创建Bokeh图形
    source = ColumnDataSource(df)
    p = figure(x_axis_label='Time (seconds)', y_axis_label='Parameter Value')
    p.line(x='Time[s]', y='ENS', source=source, legend_label='ENS', line_width=2)
    p.line(x='Time[s]', y='Trigger', source=source, legend_label='Trigger', line_width=2)
    p.line(x='Time[s]', y='IGN', source=source, legend_label='IGN', line_width=2)
    p.line(x='Time[s]', y='SAFING', source=source, legend_label='SAFING', line_width=2)

    # 将Bokeh图形嵌入到HTML中
    html_code = show(p, notebook_handle=False, serve=False)
    with open("test.html", 'w') as html_file:
        html_file.write(html_code)
    # 打印HTML代码（可选）
    print(html_code)
import plotly.express as px

def plot_interactive_square_wave_plotly(file_path):
    # 从CSV文件加载数据到DataFrame
    df = pd.read_csv(file_path)

    # 使用 Plotly Express 创建交互式图表
    fig = px.line(df, x='Time[s]', y=['ENS', 'Trigger', 'IGN', 'SAFING'], title='Interactive Binary Square Waveform Parameters')

    # 设置布局
    fig.update_layout(
        xaxis=dict(title='Time (seconds)'),
        yaxis=dict(title='Parameter Value', tickvals=[0, 1], range=[-0.1, 1.1]),
        legend=dict(x=0, y=1),
        hovermode='x unified'
    )

    # 显示交互式图表
    fig.show()

    # 将图表保存为HTML文件
    fig.write_html("plotly_table.html")
csv_file_path = "single.csv"
# plot_interactive_square_wave_with_time_diff(csv_file_path)
plot_interactive_square_wave_plotly(csv_file_path)
# result_df = analyze_ens_data(csv_file_path)
# print(result_df)
# result_df = analyze_ens_data_to_df(csv_file_path)
# print(result_df)
# result_df = analyze_ens_data_to_df5(csv_file_path)
# print(result_df)