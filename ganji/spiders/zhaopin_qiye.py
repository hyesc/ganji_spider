# -*- coding: utf-8 -*-
import json

import scrapy
import logging
from copy import deepcopy

from ganji.items import GanjiItem

logger = logging.getLogger(__name__)


class ZhaopinQiyeSpider(scrapy.Spider):
    name = 'zhaopin_qiye'
    allowed_domains = ['ganji.com']

    def start_requests(self):
        with open('ganji/河南.json', 'r') as f:
            city_list = json.loads(f.read())

        for i in city_list:
            item = GanjiItem()  # 每个城市一个item
            url = i.get('url')
            city = i.get('city')
            item['city'] = city
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={'item': item}
            )
            break

    def parse(self, response):
        """
        1.从响应中提取企业详情页的url
        2.提取下一页的url,并发送请求,调用本函数解析
        """
        # 提取企业的详情页url,发送请求
        company_detail_urls = response.xpath('//div[@class="com-list-2"]/table//a/@href').extract()
        for url in company_detail_urls:
            item = response.meta.get('item')  # 包含城市信息的item,每个公司都要有这条信息
            item['info_url'] = url  # 信息来源
            item['cid'] = 1  # TODO
            yield scrapy.Request(
                url='http://www.ganji.com/gongsi/15492211940096w/',
                callback=self.parse_detail,
                meta={'item': item}
            )
            break
            # TODO 翻页

    def parse_detail(self, response):
        """
        1.从详情页中提取公司有效信息
        2.从详情页中提取职位信息,并发起请求
        """
        item = response.meta.get('item')
        resp_url = response.url
        # 通过判断url的长度分辨响应的是哪种页面
        # 规则的 http://www.ganji.com/gongsi/106888687/   长度38
        if len(resp_url) > 28:
            # 没有重定向,extract_first前的xpath得到是空列表,默认设置我None
            print(resp_url)
            item['c_name'] = response.xpath('//div[@class="c-title"]/h1/text()').extract_first()  # 公司名称
            item['social_code'] = response.xpath(
                '//li/span[text()="统一社会代码:"]/following-sibling::*[1]/text()').extract_first()  # 统一社会代码
            item['organization_code'] = response.xpath(
                '//li/span[text()="组织机构代码:"]/following-sibling::*[1]/text()').extract_first()  # 组织机构代码
            item['register_address'] = response.xpath(
                '//li/span[text()="注册地址:"]/following-sibling::*[1]/text()').extract_first()  # 注册地址
            item['c_address'] = response.xpath('//li/em[text()="公司地址："]/../text()').extract_first()  # 公司地址
            # item['tel'] = 1  # 赶集没有这个字段
            print(item)

            # 获取职位的标签tr,如果存在,说明有职位,否则没有在招职位
            tr_list = response.xpath('//div[@class="common-list-tab mt-5"]/table//tr[position()>1]')
            if len(tr_list) > 0:
                # 请求职位url
                for tr in tr_list:
                    job_url = tr.xpath('./td[1]/a/@href').extract_first()
                    item['salary'] = tr.xpath('./td[2]/text()').extract_first()
                    item['edu'] = tr.xpath('./td[3]/text()').extract_first()
                    item['recruit_num'] = tr.xpath('./td[4]/text()').extract_first()
                    item['update_time'] = tr.xpath('./td[6]/text()').extract_first()

        elif len(resp_url) == 28:
            # 重定向,页面不存在了,item丢弃
            logger.warning('公司信息不存在,url=%s' % resp_url)
        else:
            logger.error('未知异常,url=%s' % resp_url)
