# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GanjiPhoneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 公司company表
    c_name = scrapy.Field()  # 公司名称
    social_code = scrapy.Field()  # 统一社会代码
    organization_code = scrapy.Field()  # 组织机构代码
    register_address = scrapy.Field()  # 注册地址
    c_address = scrapy.Field()  # 公司地址,基本信息中可能会有
    c_tel = scrapy.Field()  # 公司电话,赶集应该没有该数据
    cid = scrapy.Field()  # 逻辑主键,用来关联招聘表,采用uuid生成
    info_url = scrapy.Field()
    pc_url = scrapy.Field()
    create_date = scrapy.Field()
    city = scrapy.Field()
    # 招聘表recruit
    job_name = scrapy.Field()  # 职位名称
    job_address = scrapy.Field()  # 职位地址
    salary = scrapy.Field()  # 工资
    recruit_num = scrapy.Field()  # 招聘人数
    edu = scrapy.Field()  # 学历
    update_time = scrapy.Field()  #　更新时间
    job_tel = scrapy.Field()
    contact_person = scrapy.Field()
    job_url = scrapy.Field()
    # cid_j = scrapy.Field()  # 外键,cid
