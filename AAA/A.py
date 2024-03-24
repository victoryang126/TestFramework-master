import pandas as pd

def merge_columns(df):
    """
    合并以 'Req_' 开头的列，保持其他列不变。
    参数：
    df (DataFrame): 要处理的 DataFrame。
    返回：
    DataFrame: 处理后的 DataFrame，Req 列合并后的列名为 'Req'。
    """
    # 获取所有以 'Req_' 开头的列名
    req_columns = [col for col in df.columns if col.startswith('Req_')]
    # 如果没有找到以 'Req_' 开头的列，则直接返回原始 DataFrame
    if not req_columns:
        return df
    # 找到第一个 'Req_' 开头的列的位置
    req_index = df.columns.get_loc(req_columns[0])
    # 合并 'Req_' 开头的列，并创建新的 'Req' 列
    req_values = df[req_columns].apply(lambda row: {col.split('_')[1]: row[col] for col in req_columns}, axis=1)
    df.insert(req_index, 'Req', req_values)
    # 删除原来的 'Req_' 开头的列
    df.drop(columns=req_columns, inplace=True)

    return df

# 示例 DataFrame
data = {
    'stepstart': [1, 2, 3],
    'PreAction': ['action1', 'action2', 'action3'],
    'Req_SessionType': ['session1', 'session2', 'session3'],
    'Req_OtherParam': ['param1', 'param2', 'param3'],
    'PostAction': ['action1', 'action2', 'action3']
}
df = pd.DataFrame(data)

# 调用函数处理 DataFrame
df_processed = merge_columns(df)
print(df_processed.columns)
print(df_processed['Req'])
