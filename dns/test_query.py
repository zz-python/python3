# -*- coding: utf-8 -*-
import dns.resolver

def dns_query(domain):
    try:
        # 创建 DNS 查询解析器
        resolver = dns.resolver.Resolver()

        # 发送 DNS 查询，获取 A 记录
        result = resolver.resolve(domain, 'A')
        
        # 打印查询结果
        for ip in result:
            print(ip)
    
    except dns.resolver.NXDOMAIN:
        print("Domain not found")
    except dns.resolver.NoAnswer:
        print("No A record found for the domain")
    except dns.resolver.Timeout:
        print("DNS query timed out")

# 发送 DNS 查询
dns_query('baidu.com')
