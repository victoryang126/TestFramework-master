def bytearray_to_hex_list(byte_array):
    hex_list = ['0x{:02X}'.format(byte) for byte in byte_array]
    return hex_list


# byte_array = bytearray(b'\x01\x02\x0A\xFF')
#
# hex_list = bytearray_to_hex_list(byte_array)
# print(hex_list)

import os

def get_main_folder():
    main_folder = None
    if hasattr(os, 'path'):
        # 获取主模块的文件名
        main_folder = os.path.abspath(os.path.dirname(__import__('__main__').__file__))

    return main_folder

# 示例调用
main_folder = get_main_folder()
print(main_folder)


import os

def get_main_filename():
    # 获取主模块的文件路径
    main_filepath = __import__('__main__').__file__

    # 提取文件名（包括扩展名）
    main_filename = os.path.basename(main_filepath)

    return main_filename

# 示例调用
filename = get_main_filename()
print(filename)

import inspect

def get_calling_filename():
    frame = inspect.currentframe().f_back
    filename = inspect.getframeinfo(frame).filename
    print(os.path.basename(filename).split(".")[0])
    return filename

# 示例调用
filename = get_calling_filename()
print(filename)



