import numpy as np
from scipy.stats import chisquare, describe, entropy, serial_correlation
"""
NIST SP 800-90A: 这是一个关于伪随机数生成器 (PRNG) 的标准，包括了关于随机性测试的详细描述，以及测试统计特性的方法。你可以查看该标准的文档。

NIST SP 800-90B: 这是关于熵源评估的标准，通常用于真随机数生成器 (TRNG)。它包含了对熵源的评估和测试方法。你可以查看该标准的文档。

NIST SP 800-90C: 这是关于确定性随机比特生成器 (DRBG) 的标准。它描述了一些随机性测试的方法。你可以查看该标准的文档。

BSI AIS 20 & BSI AIS 31: 这些是德国国家标准机构（BSI）发布的关于随机性和密码学的标准。AIS 20 是关于真随机数生成的标准，而 AIS 31 是关于伪随机数生成的标准。你可以查找相关文档了解更多详细信息。
"""
# 生成随机数样本
random_data = np.random.random(1000)

# 计算信息熵
entropy_value = entropy(random_data, base=2)

# 计算卡方检验
chi_square_stat, chi_square_p_value = chisquare(random_data)

# 计算均值和方差
mean, var, _, _, _ = describe(random_data)

# 计算蒙特卡罗方法误差
monte_carlo_error = 0.5  # 设置最大误差
mc_error = np.abs(np.pi - 22/7)  # 示例的蒙特卡罗方法误差

# 计算串行相关性
serial_corr = serial_correlation(random_data)

# 打印结果
print(f"Entropy: {entropy_value}")
print(f"Chi-square: Statistic - {chi_square_stat}, p-value - {chi_square_p_value}")
print(f"Mean Value: {mean}")
print(f"Monte Carlo Error: {mc_error}")
print(f"Serial Correlation: {serial_corr}")
