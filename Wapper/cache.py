import functools

@functools.lru_cache(maxsize=3)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 第一次调用 fibonacci(5) 时会进行计算，并缓存结果
print(fibonacci(5))  # 输出：5

# 第二次调用 fibonacci(5) 时直接从缓存中获取结果，无需再次计算
print(fibonacci(5))  # 输出：5

# 缓存中存储了之前的计算结果
print(fibonacci.cache_info())  # 输出：CacheInfo(hits=1, misses=1, maxsize=3, currsize=1)
