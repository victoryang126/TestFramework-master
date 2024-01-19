import pandas as pd

def process_qualify_columns(df):
    # 获取所有列名
    columns = df.columns

    # 找到包含 "Qualify" 字符串的列
    qualify_columns = [col for col in columns if 'Qualify' in col]

    # 处理每个符合条件的列
    for col in qualify_columns:
        # 使用 apply 函数对每个单元格进行 split 操作
        df[col] = df[col].apply(lambda x: x.split(",") if pd.notnull(x) else x)

    return df

# 示例用法
data = {'ID': [1, 2, 3],
        'Name_Qualify1': ['A,X,Y', 'B,Z', 'C'],
        'Value_Qualify2': ['10,20,30', '40', '50,60']}
df = pd.DataFrame(data)

# 处理包含 "Qualify" 字符串的列
result_df = process_qualify_columns(df)

# 打印处理后的 DataFrame
print(result_df)
