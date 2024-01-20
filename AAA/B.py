import pandas as pd
import numpy as np

def add_merged_loop_column(data_frame):
    # 获取所有列名带有 "Loop" 的列
    loop_columns = [col for col in data_frame.columns if 'LOOP' in col]
    merged_array = data_frame[loop_columns].apply(lambda row: row.tolist(), axis=1).tolist()
    merged_array = [[val for val in row if not pd.isna(val)] for row in merged_array]
    # 将合并后的数组添加为新列
    data_frame["LOOP"] = merged_array


def add_merged_loop_column2(data_frame):
    # 获取所有列名带有 "Loop" 的列
    loop_columns = [col for col in data_frame.columns if 'LOOP' in col]
    merged_array = np.stack([data_frame[col].values for col in loop_columns],-1)
    merged_array = [[val for val in row if not pd.isna(val)] for row in merged_array]
    print(merged_array)
    data_frame["LOOP"] = merged_array



def process_and_save_to_files(data_frame, sensors, sensors_data_per_ms, output_dir):
    # 填充空值为0
    data_frame[sensors] = data_frame[sensors].fillna(0)
    # 遍历每一行
    for index, row in data_frame.iterrows():
        level = row['CrashSeverityLevel']
        # 根据传感器速率计算lineNr
        line_nr = int(row['Time'] * sensors_data_per_ms[sensors[0]])
        # 生成文件名
        file_name = f"{output_dir}/{level}_{'_'.join(sensors)}.txt"
        # 生成文件内容
        content = '\n'.join(map(str, row[sensors]))
        # 写入文件
        with open(file_name, 'w') as file:
            file.write(content)



# 示例用法
# data = pd.read_csv("test3.csv")  # 请替换为实际文件路径
# add_merged_loop_column2(data)
# # print(data['LOOP'])
data = {
    'CrashSeverityLevel': ['FRONT_LEVEL0', 'FRONT_LEVEL1', 'FRONT_LEVEL2', 'FRONT_LEVEL3', 'FRONT_LEVEL4', 'FRONT_LEVEL5'],
    'Time': [30, 40, 40, 30, 30, 15],
    'GEN6_X': [75, 125, 125, 225, 325, 425],
    'GEN6_Y': [0, 0, 0, np.NAN, 0, 0],
    'RSU_G_LtFront': [120, 0, 0, 0, 0, 120],
}

df = pd.DataFrame(data)
print(df)
# 传感器列名数组
# sensors = ['GEN6_X', 'GEN6_Y', 'RSU_G_LtFront']
# # 传感器速率字典
# sensors_data_per_ms = {"GEN6_X": 2, "GEN6_Y": 2, "RSU_G_LtFront": 4}
# # 输出文件的目录
# output_directory = 'resources'
# # 处理数据并保存到文件
# process_and_save_to_files(df, sensors, sensors_data_per_ms, output_directory)