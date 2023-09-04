# 假设你有一个bytearray的列表
bytearray_list = [bytearray(b'abc'), bytearray(b'def'), bytearray(b'abc'), bytearray(b'ghi')]

# 使用集合来去重
unique_bytearrays = list(set(bytearray_list))

# 如果你需要保持原始的字节序列顺序，可以使用OrderedDict来保持顺序
from collections import OrderedDict
unique_bytearrays_ordered = list(OrderedDict.fromkeys(bytearray_list))

# 打印去重后的结果
print(unique_bytearrays)
print(unique_bytearrays_ordered)
