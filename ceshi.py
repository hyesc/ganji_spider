import json
import re
import uuid

import requests
from lxml import etree

# url = 'http://www.ganji.com/gongsi/106897165/'  # 验证页面丢失的情况
# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
# }
# resp = requests.get(url, headers=headers)
#
# html = etree.HTML(resp.content)
# c = html.xpath('//div[@class="d-c-left"]/div[@class="c-introduce"]')  # 页面不存,得到空列表
# print(c)


# 转码问题
# b = '北京'
# c = b.encode('unicode_escape').decode()
# print(type(c))
# print(c)  # \u5317\u4eac
# a = '\u5317\u4eac'
# print(a)


# 测试uuid生成
# u1 = uuid.uuid1()
# print(u1)
#
# name = 'hy'
# print(uuid.NAMESPACE_DNS)
# # 相同的namespace和name生成相同的uuid值
# u3 = uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=name)
# print(u3)
# u3 = uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name=name)
# print(u3)


# 58 城市列表信息抽取
# url = 'http://pic2.58.com/js/v6/source/238b6adb9460b304f80e0418dfd57894_6051785045.js'  # 验证页面丢失的情况
# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
# }
# resp = requests.get(url, headers=headers)
#
# # with open('58.js', 'w') as f:
# #     f.write(resp.content.decode())
#
# ret = re.findall(r'dsy.add(.*?);', resp.content.decode())


a = 'http://www.ganji.com/gongsi/106888687/'
b = ''
print(len(a))