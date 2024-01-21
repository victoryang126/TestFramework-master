import numpy as np
import pandas as pd

def process_samples_numpy(times, values):
    # 计算当前采样点到下一个采样点的间隔时间
    durations:np.array = np.diff(times, prepend=0)
    durations_shifted = np.roll(durations,-1)
    return values, durations_shifted

def sum_every_n_elements(arr, n):
    reshaped_array = arr.reshape(-1, n)
    print(reshaped_array)
    row_sums = np.sum(reshaped_array, axis=1)
    return row_sums

def rolling_mean_numpy(arr, window_size):
    # 定义一个窗口
    window = np.ones(window_size) / window_size
    # 使用convolve计算滚动平均
    result = np.convolve(arr, window, mode='valid')
    return result

def rolling_sum_numpy(arr, window_size):
    # 定义一个窗口
    window = np.ones(window_size)
    # 使用convolve计算滚动和
    result = np.convolve(arr, window, mode='valid')

    return result

def cumulative_sum_by_step(arr, step):
    # 使用numpy.cumsum计算累积和
    # [1, 3, 3, 4, 5, 6,7, 8, 9, 10] 会输出 [ 4 11 22 37 56]
    cumulative_sums = np.cumsum(arr)
    # 计算每个步长的元素和
    step_sums = cumulative_sums[step-1::step]  # 注意索引从0开始
    print(step_sums)
    return step_sums

def cumulative_product_by_step(arr, step):
    # 使用numpy.cumprod计算累积乘积
    cumulative_products = np.cumprod(arr)
    # 计算每个步长的元素积分
    step_products = cumulative_products[step-1::step]  # 注意索引从0开始
    return step_products

def analyze_ens_data_to_df5(sample_points, sample_times):
    # 找到ENS列中当前采样点和下一个不同值的采样点的索引
    change_indices = pd.Series(sample_points).ne(pd.Series(sample_points).shift())
    # 获取不同值之间的时间间隔和值
    sample_times_diff = pd.Series(sample_times).diff().shift(-1).fillna(0).tolist()
    sample_points_filtered = pd.Series(sample_points).tolist()
    # 构建结果DataFrame
    result_df = pd.DataFrame({
        'Sample Points': sample_points_filtered,
        'Sample Times': sample_times_diff
    })

    return result_df

def analyze_ens_data_to_df5_numpy(sample_points, sample_times):
    # 将输入数组转换为 NumPy 数组
    sample_points_np = np.array(sample_points)
    sample_times_np = np.array(sample_times)

    # 找到ENS列中当前采样点和下一个不同值的采样点的索引
    change_indices = np.not_equal(sample_points_np, np.roll(sample_points_np, 1))

    # 获取不同值之间的时间间隔和值
    sample_times_diff = np.diff(sample_times_np, prepend=0)[change_indices]
    sample_points_filtered = sample_points_np[change_indices]

    # 构建结果DataFrame
    result_df = pd.DataFrame({
        'Sample Points': sample_points_filtered,
        'Sample Times': sample_times_diff
    })

    return result_df

# data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
#
# step_products_result = cumulative_product_by_step(data, step=2)
#
# print("Original Array:", data)
# print("Cumulative Product by Step (Numpy):", step_products_result)

# original_array = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
#
# result = sum_every_n_elements(original_array, n=5)
#
# print("Original Array:", original_array)
# print("Sum of Every 5 Elements:", result)
# sample_times = np.array([0, 1.2, 2.3, 3, 4])
# sample_values = np.array([10, 20, 15, 30, 25])

# result_values, result_durations = process_samples_numpy(sample_times, sample_values)
# print(result_durations)
# sample_times = np.array([0, 1, 2, 3, 4])
# sample_values = np.array([10, 20, 20, 30, 30])
#
# result_values, result_time_diffs = time_diff_for_different_values(sample_times, sample_values)
#
# # 打印结果数组
# print("Different Values:", result_values)
# print("Time Diffs:", result_time_diffs)