import os
import importlib

def import_files_from_folder(folder_path):
    # 获取文件夹中的所有文件名
    file_names = os.listdir(folder_path)

    # 遍历文件名列表
    for file_name in file_names:
        # 构建文件的绝对路径
        file_path = os.path.join(folder_path, file_name)

        # 检查文件路径是否是一个文件
        if os.path.isfile(file_path):
            # 提取文件名（不包括扩展名）作为模块名
            module_name = os.path.splitext(file_name)[0]

            # 动态导入模块
            module = importlib.import_module(module_name)

            # 可以在这里对导入的模块进行处理或使用
            # ...

# 示例调用，假设要导入的文件夹路径为 'folder_path'
folder_path = 'folder_path'
import_files_from_folder(folder_path)
