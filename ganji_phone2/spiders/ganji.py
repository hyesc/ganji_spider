import random
import json
import uuid
import scrapy
import logging
from copy import deepcopy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError
from ganji_phone2.items import GanjiPhoneItem
from ganji_phone2.settings import COOKIES
from pymongo import MongoClient

logger = logging.getLogger(__name__)
client = MongoClient()
c_job_detail = client.ganji.job_detail  # 存储带有职位信息的公司item


class GanjiSpider(scrapy.Spider):
    name = 'ganji'
    allowed_domains = ['ganji.com']

    def start_requests(self):
        with open('ganji_phone2/河南.json', 'r') as f:
            city_list = json.loads(f.read())
        # 遍历城市列表,发起请求,用于获得总共有多少页数据
        for i in city_list:
            item = GanjiPhoneItem()  # 每个城市一个item
            url = i.get('url')
            city = i.get('city')
            item['city'] = city
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={'item': item},
                cookies=random.choice(COOKIES)
            )

    def parse(self, response):
        """从响应中提取出来max_page,构造所有页的url,发起请求"""
        item = response.meta.get('item')
        info_dict = json.loads(response.text)
        resp_url = response.url
        max_page = info_dict.get('page').get('max_page')
        logger.warning(max_page)
        # 请求所有的页面,包括第一页
        for i in range(1, int(max_page) + 1):
            url = resp_url.replace('P1', 'P%d' % i)
            yield scrapy.Request(
                url,
                callback=self.create_c_url,
                meta={'item': item},
            )

    def create_c_url(self, response):
        """从响应的json中,提取公司id,构造公司详情页url,发起请求"""
        item = response.meta.get('item')
        # 获取公司id,构造公司详情url,发起请求
        info_dict = json.loads(response.text)
        for c in info_dict.get('list'):
            c_id = c.get('company_id')
            c_url = 'https://3g.ganji.com/gongsi_{}/'.format(c_id)
            item['cid'] = str(uuid.uuid1())
            item['info_url'] = c_url
            yield scrapy.Request(
                c_url,
                callback=self.parse_detail,
                meta={'item': deepcopy(item), 'page1_requested': True},  # 每家公司一个item
                errback=self.parse_err,
            )

    def parse_detail(self, response):
        """处理公司详情页的数据,根据url长度判断属于何种响应结构,带注册信息的响应结构没有电话,招聘信息可有可无,以实际为准,
           不带注册结构的,pc端有公司地址,移动端有电话号码,分别请求提取
        """
        print('^' * 50)
        resp_url = response.url
        item = response.meta.get('item')

        if len(resp_url) == 38:
            # http://3g.ganji.com/zz_wanted/  重定向的丢弃,不做任何操作
            c_name = response.xpath('//div[@class="com-name"]/text()').extract_first()  # 公司名称
            item['c_name'] = c_name.strip() if c_name else c_name
            item['social_code'] = response.xpath(
                '//li/span[text()="统一社会信用代码"]/following-sibling::*[1]/text()').extract_first()  # 统一社会代码
            item['organization_code'] = response.xpath(
                '//li/span[text()="组织机构代码"]/following-sibling::*[1]/text()').extract_first()  # 组织机构代码
            item['register_address'] = response.xpath(
                '//li/span[text()="注册地址"]/following-sibling::*[1]/text()').extract_first()  # 注册地址
            # 成立日期字段没有意义,仅仅是区别与没有注册信息的公司的item字段数量
            item['create_date'] = response.xpath(
                '//span[text()="建立日期"]/following-sibling::*[1]/text()').extract_first()  # 成立日期
            # 招聘职位url
            job_urls = response.xpath(
                '//div[@class="job-contain"]//div[@class="deliver-area"]/a[@class="infor"]/@href').extract()

            if job_urls:
                # 在此处把item另存一份到mongo中,单独写爬虫读取url再次请求
                print('有注册结构,有招聘信息,存入数据库,单独请求')
                c_job_detail.insert(dict(item))
            else:
                print('有注册结构,企业无招聘的item')
                yield item
        # 以w/结尾的url,公司详情页面结构和上边的不同,没有任何注册信息,但是手机端有电话,pc端有公司地址,分别请求
        elif resp_url.endswith('w/'):
            c_name = response.xpath('//div[@class="com-name"]/text()').extract_first()  # 公司名称
            item['c_name'] = c_name.strip() if c_name else c_name
            item['c_tel'] = response.xpath(
                '//th[text()="联系电话"]/following-sibling::*[1]/a/text()').extract_first()  # gongsidianhua
            pc_detail_url = 'http://www.ganji.com/gongsi/{}'.format(resp_url.split('_')[-1])
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
            }

            yield scrapy.Request(
                pc_detail_url,
                callback=self.parse_pc_detail,
                meta={'item': item},  # 没有职位信息,一个公司就是一条item
                headers=headers,
                errback=self.parse_err,
            )
        else:
            logger.error(response)

    def parse_pc_detail(self, response):
        """以w/结尾的url,需要重新请求pc端来获取公司地址"""
        print('p' * 50)
        item = response.meta.get('item')
        item['pc_url'] = response.url
        item['c_address'] = response.xpath('//li/em[text()="公司地址："]/../text()').extract_first()  # 公司地址
        print('响应中不带注册结构,没有任何招聘信息的item')
        yield item

    def parse_err(self, failure):
        """处理非正常请求"""
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response

            logger.error(
                'HttpError on %s' % response.url)  # HttpError on https://3g.ganji.com/zz_jzchuandanpaifa/2984061273x?ifid=seo_company_detail

        elif failure.check(DNSLookupError):
            request = failure.request
            logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            logger.error('TimeoutError on %s', request.url)
