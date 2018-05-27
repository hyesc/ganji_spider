import hashlib
import re
import redis
import scrapy
import logging
from copy import deepcopy
from scrapy.exceptions import CloseSpider
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.utils.python import to_bytes
from twisted.internet.error import DNSLookupError, TCPTimedOutError
from w3lib.url import canonicalize_url
from pymongo import MongoClient

logger = logging.getLogger(__name__)
# mongodb数据库连接
client = MongoClient()
collection = client.ganji.job_detail  # 放入有招聘信息的公司item

# redis连接,处理异常时删除异常请求的指纹
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=2)


class JobSpider(scrapy.Spider):
    name = 'job'
    allowed_domains = ['ganji.com']
    count = 1

    def start_requests(self):
        """从mongo中读出来数据"""
        item_cursor = collection.find({})
        for item in item_cursor:
            item.pop('_id')
            info_url = item.get('info_url')
            yield scrapy.Request(
                info_url,  # 此时不会被反爬
                callback=self.parse_detail,
                meta={'item': item},  # 每个公司一个item
            )

    def parse_detail(self, response):
        """提取职位url并发起请求"""
        item = response.meta.get('item')
        job_urls = response.xpath(
            '//div[@class="job-contain"]//div[@class="deliver-area"]/a[@class="infor"]/@href').extract()
        if job_urls:
            for job_url in job_urls:
                url = 'https:' + job_url
                # print('job_url', url, JobSpider.count)
                # JobSpider.count += 1
                yield scrapy.Request(
                    url,  # 此处会被反爬
                    callback=self.parse_job_detail,
                    meta={'item': deepcopy(item), 'dont_redirect': True},  # 每个职位一条item
                    errback=self.parse_err,
                )
            # 翻页处理
            next_url = response.xpath('//a[@class="page-down"]/@href').extract_first()
            if next_url:
                next_url = response.urljoin(next_url)
                yield scrapy.Request(
                    next_url,
                    callback=self.parse_detail,
                    meta={'item': item},  # item不变,还是原来的item,在对详情页请求时深拷贝
                    dont_filter=True,  # 不可过滤,否则一旦反爬,重新运行代码麻烦
                )

    def parse_job_detail(self, response):
        """移动端职位详情页数据提取"""
        # 能进行到这一步的,说明没有重定向,正常保存即可
        resp_url = response.url
        item = response.meta.get('item')
        item['job_url'] = resp_url
        item['salary'] = response.xpath('//div[@class="fl fc-red"]/text()').extract_first()
        require = response.xpath(
            '//th[text()="要求"]/../td').extract_first()  # https://3g.ganji.com/heze_zpsiji/3203839155x?ifid=seo_company_detail&wapadprurl2=adurl
        ret = re.match(r'<td>(.*)</td>', require, re.S)
        if ret:
            ret = ret.group(1)
            require_list = ret.split('<span class="s"></span>')
            item['recruit_num'] = require_list[0].strip().replace('人', '')
            item['edu'] = require_list[1].strip()
        item['update_time'] = response.xpath(
            '//div[@class="fr mlr5"]/span[@class="fc8d f12"]/text()').extract_first()
        item['job_name'] = response.xpath('//h1[@class="title"]/text()').extract_first()
        item['job_address'] = response.xpath('//th[text()="地点"]/following-sibling::*[1]/text()').extract_first()
        # 对地址信息进行处理,防止地址不存在的情况,不存在就不设置这个字段
        item['job_tel'] = response.xpath(
            '//em[@style="padding: 0 0.5em;"]/../following-sibling::*[1]/text()').extract_first()
        item['contact_person'] = response.xpath('//th[text()="联系人"]/following-sibling::*[1]/text()').extract_first()
        print('有注册结构,并且有注册信息的item, parse_job_detail')
        yield item  # item同样存入ganji_phone这个集合中

    def parse_err(self, failure):
        """处理非正常请求"""
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            # req = failure.request  req.url == response.url
            response = failure.value.response
            item = response.meta.get('item')  # 这里可以拿到response中携带的item信息
            print('resp_url', response.url)
            print(item)
            logger.error(
                'HttpError on %s' % response.url)
            # 从redis中删除对应的过滤指纹信息
            JobSpider.del_fingerprint(response.url)  # 删除被反爬的职位详情页url对应的指纹
            JobSpider.del_fingerprint(item.get('info_url'))  # 删除公司详情页url对应的指纹
            raise CloseSpider

        elif failure.check(DNSLookupError):  # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

    @staticmethod
    def del_fingerprint(url):
        """请求失败,删除redis中的指纹"""
        fp = hashlib.sha1()
        fp.update(to_bytes('GET'))
        fp.update(to_bytes(canonicalize_url(url)))
        fp.update(b'')
        # print(fp.hexdigest())
        # 这里存的是本爬虫的url指纹集合
        r.srem('job:dupefilter', fp.hexdigest())
