# -*-coding:utf-8-*-
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import string
import re
from items import *
from scrapy.selector import Selector


class salary_spider(scrapy.Spider):
    name = "nba"
    start_urls = ['https://www.basketball-reference.com/players/' + x + '/' for x in string.ascii_lowercase]
    #start_urls = ['https://www.basketball-reference.com/players/a/']

    def parse(self, response, *args, **kwargs):
        for player in response.xpath('//*[@id="players"]/tbody//tr'):
            link = player.xpath('./th//a/@href')[0]
            begin_year = player.xpath('.//*[@data-stat="year_min"]/text()').extract()[0]
            end_year = player.xpath('.//*[@data-stat="year_max"]/text()').extract()[0]

            if int(end_year) >= 2009:
                yield response.follow(link, self.parse_salary)

    def parse_salary(self, response):
        name = response.xpath('//*[@itemprop="name"]/span/text()').extract()[0]
        born = response.xpath('//*[@itemprop="birthDate"]/@data-birth').extract()[0] \
            if len(response.xpath('//*[@itemprop="birthDate"]/@data-birth').extract()) > 0 else ''

        table = response.xpath('//*[@id="all_all_salaries"]').extract()[0] \
            if len(response.xpath('//*[@id="all_all_salaries"]').extract()) > 0 else ''
        table = re.sub('<!--', '', table)
        table = re.sub('-->', '', table)
        table = Selector(text=table).xpath('.//tbody')

        for row in table.xpath('.//tr'):
            salary = {}
            salary['Name'] = name
            salary['Born'] = born
            salary['Season'] = row.xpath('.//*[@data-stat="season"]/text()').extract()[0]
            if int(salary['Season'].split('-')[0]) > 2020 or int(salary['Season'].split('-')[0]) < 2009:
                continue
            salary['Team'] = row.xpath('.//*[@data-stat="team_name"]/a/text()').extract()[0]
            salary['Lg'] = row.xpath('.//*[@data-stat="lg_id"]/a/text()').extract()[0]
            salary['Salary'] = row.xpath('.//*[@data-stat="salary"]/text()').extract()[0]
            salary['Salary'] = re.sub(r'[$,]', '', salary['Salary'])

            yield salary