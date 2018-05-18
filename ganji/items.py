# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GanjiItem(scrapy.Item):
    # 基本信息
    # city = scrapy.Field()  # 城市名
    # c_size = scrapy.Field()  # 公司规模
    # c_industry = scrapy.Field()  # 公司行业
    # c_type = scrapy.Field()  # 公司类型
    # c_website = scrapy.Field()  # 公司网站
    # 注册信息
    # establish_date = scrapy.Field()  # 成立日期
    # operate_period = scrapy.Field()  # 经营期限
    # registration_authority = scrapy.Field()  # 登记机关
    # business_status = scrapy.Field()  # 经营状态
    # register_capital = scrapy.Field()  # 注册资本
    # enterprise_type = scrapy.Field()  # 企业类型

    # 公司company表
    c_name = scrapy.Field()  # 公司名称
    social_code = scrapy.Field()  # 统一社会代码
    organization_code = scrapy.Field()  # 组织机构代码
    register_address = scrapy.Field()  # 注册地址
    c_address = scrapy.Field()  # 公司地址,基本信息中可能会有
    tel = scrapy.Field()  # 公司电话,赶集应该没有该数据
    cid = scrapy.Field()  # 逻辑主键,用来关联招聘表,采用uuid生成
    info_url = scrapy.Field()
    # 招聘表recruit
    job_name = scrapy.Field()  # 职位名称
    job_address = scrapy.Field()  # 职位地址
    city = scrapy.Field()
    salary = scrapy.Field()  # 工资
    recruit_num = scrapy.Field()  # 招聘人数
    edu = scrapy.Field()  # 学历
    update_time = scrapy.Field()  #　更新时间
    cid_j = scrapy.Field()  # 外键,cid
