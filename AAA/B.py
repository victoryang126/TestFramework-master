import pandas as pd


def generate_txt_files(data_frame):
    # 以 CrashSeverityLevel 列为键，将 Loop 相关的列合并成一个数组
    loop_columns = [col for col in data_frame.columns if 'Loop' in col]
    merged_loop = data_frame.groupby('CrashSeverityLevel')[loop_columns].apply(lambda x: x.values.flatten()).reset_index(name='MergedLoop')

    # 生成 txt 文件
    for index, row in data_frame.iterrows():
        crash_level = row['CrashSeverityLevel']
        time = row['Time']

        # 生成文件名
        file_name = f"{crash_level}_{time}.txt"

        # 生成文件内容
        content = [f"{time * rate}\n" for rate in range(1, len(row) - 2) if isinstance(row[rate], (int, float))]

        # 写入文件
        with open(file_name, 'w') as file:
            file.writelines(content)

    # 返回合并后的 Loop 列数据
    return merged_loop

data = pd.read_csv("test.csv")  # 请替换为实际文件路径
print(data)
merged_loop_data = generate_txt_files(data)
print("Merged Loop Data:")
print(merged_loop_data)