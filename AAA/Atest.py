import pandas as pd
import io

# 从字符串创建DataFrame对象
data = '''ID,1,2,3,4,5
Incident,11s,22,33,44,55
Incident,111,222,333,444,555
Result,Pass,Failed,Pass,Failed,Pass
Result,Failed,Failed,Pass,Failed,Pass'''

df = pd.read_csv(io.StringIO(data))
print(df)
df["1"] = "11\n22"
# 使用透视表对数据进行处理
df_pivot = pd.pivot_table(df, index='ID', aggfunc=lambda x: '\n'.join(x.dropna()))

print(df_pivot)
