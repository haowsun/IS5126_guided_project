# -*-coding:utf-8-*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import string
import re
from items import *
from scrapy.selector import Selector


class gamehigh_spider(scrapy.Spider):
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


        table = response.xpath('//*[starts-with(@id, "all_highs")]').extract()[0] \
            if len(response.xpath('//*[starts-with(@id, "all_highs")]').extract()) > 0 else ''
        table = re.sub('<!--', '', table)
        table = re.sub('-->', '', table)
        table = Selector(text=table)

        for p in table.xpath('.//*[@id="highs-reg-season"]//tbody//tr'):
            #print(p.extract())
            performance = {}
            performance['Name'] = name
            performance['Born'] = born
            performance['Is_playoff'] = '0'
            performance['Season'] = p.xpath('.//*[@data-stat="season"]/a/text()').extract()[0]
            if int(performance['Season'].split('-')[0]) > 2020 or int(performance['Season'].split('-')[0]) < 2009:
                continue
            performance['Age'] = p.xpath('.//*[@data-stat="age"]/text()').extract()[0]
            performance['Tm'] = p.xpath('.//*[@data-stat="team"]/a/text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="team"]/a/text()').extract()) > 0 \
                else p.xpath('.//*[@data-stat="team"]/text()').extract()[0]
            performance['Lg'] = self.fun(p, './/*[@data-stat="league"]/a/text()')
            performance['MP'] = self.fun(p, './/*[@data-stat="time_on_court"]//text()')
            performance['FG'] = self.fun(p, './/*[@data-stat="fg"]//text()')
            performance['FGA'] = self.fun(p, './/*[@data-stat="fga"]//text()')
            performance['3P'] = self.fun(p, './/*[@data-stat="fg3"]//text()')
            performance['3PA'] = self.fun(p, './/*[@data-stat="fg3a"]//text()')
            performance['2P'] = self.fun(p, './/*[@data-stat="fg2"]//text()')
            performance['2PA'] = self.fun(p, './/*[@data-stat="fg2a"]//text()')
            performance['FT'] = self.fun(p, './/*[@data-stat="ft"]//text()')
            performance['FTA'] = self.fun(p, './/*[@data-stat="fta"]//text()')
            performance['ORB'] = self.fun(p, './/*[@data-stat="orb"]//text()')
            performance['DRB'] = self.fun(p, './/*[@data-stat="drb"]//text()')
            performance['TRB'] = self.fun(p, './/*[@data-stat="trb"]//text()')
            performance['AST'] = self.fun(p, './/*[@data-stat="ast"]//text()')
            performance['STL'] = self.fun(p, './/*[@data-stat="stl"]//text()')
            performance['BLK'] = self.fun(p, './/*[@data-stat="blk"]//text()')
            performance['TOV'] = self.fun(p, './/*[@data-stat="tov"]//text()')
            performance['PF'] = self.fun(p, './/*[@data-stat="pf"]//text()')
            performance['PTS'] = self.fun(p, './/*[@data-stat="pts"]//text()')
            performance['GmSc'] = self.fun(p, './/*[@data-stat="game_score"]//text()')

            #print(performance)
            yield performance

        for p in table.xpath('.//*[@id="highs-playoffs"]//tbody//tr'):
            # print(p.extract())
            performance = {}
            performance['Name'] = name
            performance['Born'] = born
            performance['Is_playoff'] = '1'
            performance['Season'] = p.xpath('.//*[@data-stat="season"]/a/text()').extract()[0]
            if int(performance['Season'].split('-')[0]) > 2020 or int(performance['Season'].split('-')[0]) < 2009:
                continue
            performance['Age'] = p.xpath('.//*[@data-stat="age"]/text()').extract()[0]
            performance['Tm'] = p.xpath('.//*[@data-stat="team"]/a/text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="team"]/a/text()').extract()) > 0 \
                else p.xpath('.//*[@data-stat="team"]/text()').extract()[0]
            performance['Lg'] = self.fun(p, './/*[@data-stat="league"]/a/text()')
            performance['MP'] = self.fun(p, './/*[@data-stat="time_on_court"]//text()')
            performance['FG'] = self.fun(p, './/*[@data-stat="fg"]//text()')
            performance['FGA'] = self.fun(p, './/*[@data-stat="fga"]//text()')
            performance['3P'] = self.fun(p, './/*[@data-stat="fg3"]//text()')
            performance['3PA'] = self.fun(p, './/*[@data-stat="fg3a"]//text()')
            performance['2P'] = self.fun(p, './/*[@data-stat="fg2"]//text()')
            performance['2PA'] = self.fun(p, './/*[@data-stat="fg2a"]//text()')
            performance['FT'] = self.fun(p, './/*[@data-stat="ft"]//text()')
            performance['FTA'] = self.fun(p, './/*[@data-stat="fta"]//text()')
            performance['ORB'] = self.fun(p, './/*[@data-stat="orb"]//text()')
            performance['DRB'] = self.fun(p, './/*[@data-stat="drb"]//text()')
            performance['TRB'] = self.fun(p, './/*[@data-stat="trb"]//text()')
            performance['AST'] = self.fun(p, './/*[@data-stat="ast"]//text()')
            performance['STL'] = self.fun(p, './/*[@data-stat="stl"]//text()')
            performance['BLK'] = self.fun(p, './/*[@data-stat="blk"]//text()')
            performance['TOV'] = self.fun(p, './/*[@data-stat="tov"]//text()')
            performance['PF'] = self.fun(p, './/*[@data-stat="pf"]//text()')
            performance['PTS'] = self.fun(p, './/*[@data-stat="pts"]//text()')
            performance['GmSc'] = self.fun(p, './/*[@data-stat="game_score"]//text()')

            # print(performance)
            yield performance

    def fun(self, p, pattern):
        return p.xpath(pattern).extract()[0] if len(p.xpath(pattern).extract()) > 0 else ''
