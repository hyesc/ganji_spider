# -*- coding: utf-8 -*-
import json

import scrapy
import logging
from copy import deepcopy

from ganji.items import GanjiItem

logger = logging.getLogger(__name__)

# 初版写法,获取所有城市
class ZhaopinQiyeSpider(scrapy.Spider):
    name = 'zhaopin_qiye_bat'
    allowed_domains = ['ganji.com']
    # start_urls = ['http://www.ganji.com/index.htm?goto=gongsi/']  # 城市页面作为起始页面


    # def parse(self, response):
    #     """从响应中提取出来所有城市的url,构造对应的公司的url,并发起请求"""
    #     a_city = response.xpath('//div[@class="all-city"]//dd/a')
    #
    #     for a in a_city:
    #         item = GanjiItem()
    #         city_url = a.xpath('./@href').extract_first()
    #         city_name = a.xpath('./text()').extract_first()
    #         item['city'] = city_name
    #         city_gongsi_url = city_url + 'gongsi/'
    #         yield scrapy.Request(
    #             city_gongsi_url,
    #             callback=self.parse_gongsi,
    #             meta={'item': item}
    #             # dont_filter=True  # 如果需要重复爬取,需要设置此项
    #         )
    #         break
    #
    # def parse_gongsi(self, response):
    #     """
    #     1.从响应中提取企业详情页的url
    #     2.提取下一页的url,并发送请求,调用本函数解析
    #     """
    #     # 提取企业的详情页url,发送请求
    #     item = response.meta.get('item')
    #     gongsi_detail_url = response.xpath('//div[@class="com-list-2"]/table//a/@href').extract()
    #     for url in gongsi_detail_url:
    #         yield scrapy.Request(
    #             url,
    #             callback=self.parse_detail,
    #             meta={'item': deepcopy(item)}  # 每个公司都会有城市信息,所以要深拷贝,保证每个item都是唯一的
    #         )
    #         break
    #         # TODO 翻页
    #
    # def parse_detail(self, response):
    #     """从详情页中提取公司有效信息"""
    #     item = response.meta.get('item')
    #     # 下边div个数可能为1,也可能为2,看是否有注册信息,不同情况得到的页面结构是不同的,应分别对待
    #     introduces = response.xpath('//div[@class="d-c-left"]/div[@class="c-introduce"]')
    #     if len(introduces) > 1:
    #         # 存在注册信息,提取数据
    #         # 基本信息
    #         item['c_name'] = 1  # 公司名称
    #         item['c_size'] = 1  # 公司规模
    #         item['c_industry'] = 1  # 公司行业
    #         item['c_type'] = 1  # 公司类型
    #         item['c_website'] = 1  # 公司网站
    #         # 注册信息
    #         item['social_code'] = 1  # 统一社会代码
    #         item['establish_date'] = 1  # 成立日期
    #         item['organization_code'] = 1  # 组织机构代码
    #         item['operate_period'] = 1  # 经营期限
    #         item['registration_authority'] = 1  # 登记机关
    #         item['business_status'] = 1  # 经营状态
    #         item['register_address'] = 1  # 注册地址
    #         item['register_capital'] = 1  # 注册资本
    #         item['enterprise_type'] = 1  # 企业类型
    #     elif len(introduces) == 1:
    #         # 不存在注册信息,有且仅有5条基本信息
    #         item['c_name'] = 1  # 公司名称
    #         item['c_size'] = 1  # 公司规模
    #         item['c_industry'] = 1  # 公司行业
    #         item['c_type'] = 1  # 公司类型
    #         item['c_address'] = 1  # 公司地址
    #     else:
    #         # 页面丢失,公司信息不存在,结果是0,忽略此公司信息,记录此公司url
    #         logger.warning('公司信息不存在,url=%s' % response.url)

