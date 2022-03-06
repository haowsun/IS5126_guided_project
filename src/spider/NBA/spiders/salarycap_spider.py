# -*-coding:utf-8-*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import re
from items import *
from scrapy.selector import Selector


class salarycap_spider(scrapy.Spider):
    name = "salarycap"
    start_urls = ['https://www.basketball-reference.com/contracts/salary-cap-history.html']

    def parse(self, response, *args, **kwargs):
        table = response.xpath('//*[@id="all_salary_cap_history"]').extract()[0] \
            if len(response.xpath('//*[@id="all_salary_cap_history"]').extract()) > 0 else ''
        table = re.sub('<!--', '', table)
        table = re.sub('-->', '', table)
        table = Selector(text=table)
        for data in table.xpath('.//tr'):
            salary_cap = {}
            salary_cap['Year'] = self.fun(data, './/*[@data-stat="year_id"]/a/text()')
            if salary_cap['Year'].split('-')[0].isdigit() is False or \
                    int(salary_cap['Year'].split('-')[0]) > 2020 or int(salary_cap['Year'].split('-')[0]) < 2009:
                continue
            salary_cap['Salary_Cap'] = self.fun(data, './/*[@data-stat="cap"]/text()').replace(',', '').replace('$', '')
            salary_cap['2021_Dollars'] = self.fun(data, './/*[@data-stat="cap2021"]/text()').replace(',', '').replace('$', '')
            print(data)
            yield salary_cap

    def fun(self, p, pattern):
        return p.xpath(pattern).extract()[0] if len(p.xpath(pattern).extract()) > 0 else ''