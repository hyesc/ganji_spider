### 运行顺序
- 先运行utils中的get_city,传入省份信息,得到省内包含的市的信息,存入json文件中（本代码仅实现河南一地的数据）
- 运行name=ganji的爬虫,爬取完成,数据存储在ganji_phone(数据最终存储位置)集合中,公司信息item存储在job_detail集合中
- 调用name=job的爬虫,如果出现重定向,即被反爬,代码终止,数据存储在test_job集合中(可改代码直接存到ganji_phone)
- 在log中查看最后请求失败的url,在浏览器打开进行验证
- 此时重新运行此爬虫,直到程序正常运行完成,没有出现反爬虫.
- 运行utils中的test_job2ganji_phone,将数据合并


### 数据保存
- 将test_job数据合并到ganji_phone中,同时修改源代码,更改需要插入的数据库,至此完成本项目数据抓取工作
- test_job 中保存的item是请求职位信息后的结果
- job_detail中保存的是有招聘的所有公司的item
- ganji_phone中保存的是所有的item最终结果

- job:dupefilter保存的是职位详情url和公司页面url
- ganji:dupefilter保存的是除了有招聘信息的公司之外的所有请求
