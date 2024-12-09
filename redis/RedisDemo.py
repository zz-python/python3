import redis

# 连接到 Redis
redis_client = redis.StrictRedis(
    host='127.0.0.1',   # Redis 服务器地址
    port=6379,          # Redis 端口，默认为 6379
    db=0,               # 使用的数据库，默认为 0
    decode_responses=True  # 自动将字节数据解码为字符串
)

# 设置示例数据（可选，用于测试）
# redis_client.set("key1", "value1")
# redis_client.lpush("list1", "item1", "item2", "item3")
# redis_client.hset("hash1", "field1", "value1")

# 读取字符串类型数据
value = redis_client.get("ACCESS:SESSIONID:SN:H1TD4T7015103")
print(f"String value: {value}")

# 读取列表类型数据
# list_items = redis_client.lrange("list1", 0, -1)
# print(f"List items: {list_items}")

# 读取哈希类型数据
# hash_value = redis_client.hget("hash1", "field1")
# print(f"Hash field value: {hash_value}")

# 获取所有键名（可选）
# all_keys = redis_client.keys()
# print(f"All keys in Redis: {all_keys}")

redis_client.connection_pool.disconnect()
