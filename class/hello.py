#!/usr/bin/python3
# coding=gbk 
class MyClass:
    """һ���򵥵���ʵ��"""
    i = 123457
    def f(self):
        return 'hello world'
 
# ʵ������
x = MyClass()
 
# ����������Ժͷ���
print("MyClass ������� i Ϊ��", x.i)
print("MyClass ��ķ��� f ���Ϊ��", x.f())
