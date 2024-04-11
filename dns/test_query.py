# -*- coding: utf-8 -*-
import dns.resolver

def dns_query(domain):
    try:
        # ���� DNS ��ѯ������
        resolver = dns.resolver.Resolver()

        # ���� DNS ��ѯ����ȡ A ��¼
        result = resolver.resolve(domain, 'A')
        
        # ��ӡ��ѯ���
        for ip in result:
            print(ip)
    
    except dns.resolver.NXDOMAIN:
        print("Domain not found")
    except dns.resolver.NoAnswer:
        print("No A record found for the domain")
    except dns.resolver.Timeout:
        print("DNS query timed out")

# ���� DNS ��ѯ
dns_query('baidu.com')
