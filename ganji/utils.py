"""
此代码执行一次,将获取到的省对应的城市的url写入文件保存即可,其他地方需要,直接从文件读取.
"""
import json
import re
import requests


def get_city(province='河南'):
    """
    用来获取对应省份的所有城市的url和城市名
    :param province: 需要获取城市的省份
    :return:返回包含每个城市信息的列表,格式为[{"city":"郑州", "url":"http://zz....."},{}]
    """
    base_url = 'http://{}.ganji.com/gongsi/'  # 用来构造城市对应的url
    url = 'http://sta.ganjistatic1.com/public/app/ms/changecity/index.cmb.js'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    city_list = list()  # 存储城市列表
    resp = requests.get(url, headers=headers)
    if resp and resp.status_code == 200:
        # 响应中正则匹配城市信息
        ret = re.match(r'window.provData=(.*?);GJ', resp.content.decode())
        if ret:
            city_str = ret.group(1).replace('city', '"city"')
            city_str = city_str.replace('name', '"name"')
            city_str = city_str.replace('date', '"date"')
            city_dict = json.loads(city_str)  # 得到包含所有省市的字典

            for city in city_dict.values():
                # 只取出需要的省的城市
                if isinstance(city, dict) and city.get('name') == province:
                    # 取出城市的代号,拼接url得到每个城市对应的url
                    for i in city.get('city'):
                        city_info = dict()  # 存储省市的字典
                        city = i[1]
                        city_url = base_url.format(i[2])
                        city_info['city'] = city
                        city_info['url'] = city_url
                        city_list.append(city_info)
                    break
            else:
                print('省份信息有误,请重新输入')
                return
    with open('{}.json'.format(province), 'w') as f:
        f.write(json.dumps(city_list, indent=2, ensure_ascii=False))
    return city_list

if __name__ == '__main__':
    get_city()
