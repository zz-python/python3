import functools

# 使用 lru_cache 装饰器来缓存结果
@functools.lru_cache()  # maxsize=None 表示没有缓存大小限制
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(30))
