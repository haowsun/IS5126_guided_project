# -*-coding:utf-8-*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import string
import re
from items import *
from scrapy.selector import Selector


class playoff_spider(scrapy.Spider):
    name = "nba"
    start_urls = ['https://www.basketball-reference.com/players/' + x + '/' for x in string.ascii_lowercase]
    #start_urls = ['https://www.basketball-reference.com/players/a/']

    def parse(self, response, *args, **kwargs):
        for player in response.xpath('//*[@id="players"]/tbody//tr'):
            link = player.xpath('./th//a/@href')[0]
            begin_year = player.xpath('.//*[@data-stat="year_min"]/text()').extract()[0]
            end_year = player.xpath('.//*[@data-stat="year_max"]/text()').extract()[0]

            if int(end_year) >= 2009:
                yield response.follow(link, self.parse_performance)

    def parse_performance(self, response):
        name = response.xpath('//*[@itemprop="name"]/span/text()').extract()[0]
        born = response.xpath('//*[@itemprop="birthDate"]/@data-birth').extract()[0] \
            if len(response.xpath('//*[@itemprop="birthDate"]/@data-birth').extract()) > 0 else ''


        table = response.xpath('//*[starts-with(@id, "all_playoffs-series")]').extract()[0] \
            if len(response.xpath('//*[starts-with(@id, "all_playoffs-series")]').extract()) > 0 else ''
        table = re.sub('<!--', '', table)
        table = re.sub('-->', '', table)
        table = Selector(text=table)

        for p in table.xpath('.//*[@id="playoffs-series"]//tbody//tr'):
            #print(name, p.extract())
            performance = {}
            performance['Name'] = name
            performance['Born'] = born
            performance['Year'] = self.fun(p, './/*[@data-stat="year"]/a/text()')
            if len(performance['Year']) == 0:
                continue
            if int(performance['Year']) > 2020 or int(performance['Year']) < 2009:
                continue
            performance['Age'] = p.xpath('.//*[@data-stat="age"]/text()').extract()[0]
            performance['Team'] = p.xpath('.//*[@data-stat="team_id"]/a/text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="team_id"]/a/text()').extract()) > 0 \
                else p.xpath('.//*[@data-stat="team_id"]/text()').extract()[0]
            performance['Lg'] = self.fun(p, './/*[@data-stat="lg_id"]/a/text()')
            performance['Round'] = self.fun(p, './/*[@data-stat="round_id"]/text()')
            performance['W/L'] = self.fun(p, './/*[@data-stat="result"]//text()')
            performance['Opp'] = self.fun(p, './/*[@data-stat="opp_id"]//text()')
            performance['G'] = self.fun(p, './/*[@data-stat="g"]//text()')
            performance['W'] = self.fun(p, './/*[@data-stat="wins"]//text()')
            performance['L'] = self.fun(p, './/*[@data-stat="losses"]//text()')
            performance['MP'] = self.fun(p, './/*[@data-stat="mp"]//text()')
            performance['FG'] = self.fun(p, './/*[@data-stat="fg"]//text()')
            performance['FGA'] = self.fun(p, './/*[@data-stat="fga"]//text()')
            performance['3P'] = self.fun(p, './/*[@data-stat="fg3"]//text()')
            performance['3PA'] = self.fun(p, './/*[@data-stat="fg3a"]//text()')
            performance['FT'] = self.fun(p, './/*[@data-stat="ft"]//text()')
            performance['FTA'] = self.fun(p, './/*[@data-stat="fta"]//text()')
            performance['ORB'] = self.fun(p, './/*[@data-stat="orb"]//text()')
            performance['TRB'] = self.fun(p, './/*[@data-stat="trb"]//text()')
            performance['AST'] = self.fun(p, './/*[@data-stat="ast"]//text()')
            performance['STL'] = self.fun(p, './/*[@data-stat="stl"]//text()')
            performance['BLK'] = self.fun(p, './/*[@data-stat="blk"]//text()')
            performance['TOV'] = self.fun(p, './/*[@data-stat="tov"]//text()')
            performance['PF'] = self.fun(p, './/*[@data-stat="pf"]//text()')
            performance['PTS'] = self.fun(p, './/*[@data-stat="pts"]//text()')
            performance['FG%'] = self.fun(p, './/*[@data-stat="fg_pct"]//text()')
            performance['3P%'] = self.fun(p, './/*[@data-stat="fg3_pct"]//text()')
            performance['FT%'] = self.fun(p, './/*[@data-stat="ft_pct"]//text()')
            performance['MP_PerG'] = self.fun(p, './/*[@data-stat="mp_per_g"]//text()')
            performance['PTS_PerG'] = self.fun(p, './/*[@data-stat="pts_per_g"]//text()')
            performance['TRB_PerG'] = self.fun(p, './/*[@data-stat="trb_per_g"]//text()')
            performance['AST_PerG'] = self.fun(p, './/*[@data-stat="ast_per_g"]//text()')

            #print(performance)
            yield performance

    def fun(self, p, pattern):
        return p.xpath(pattern).extract()[0] if len(p.xpath(pattern).extract()) > 0 else ''
