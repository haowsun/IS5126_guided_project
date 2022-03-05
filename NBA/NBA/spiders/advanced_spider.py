# -*-coding:utf-8-*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import string
import re
from items import *
from scrapy.selector import Selector


class advanced_spider(scrapy.Spider):
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

        for p in response.xpath('.//tr[starts-with(@id, "advanced")]'):
            #print(p.extract())
            performance = {}
            performance['Name'] = name
            performance['Born'] = born
            performance['Is_playoff'] = '0'
            performance['Season'] = p.xpath('.//*[@data-stat="season"]/a/text()').extract()[0]
            if int(performance['Season'].split('-')[0]) > 2020 or int(performance['Season'].split('-')[0]) < 2009:
                continue
            performance['Age'] = p.xpath('.//*[@data-stat="age"]/text()').extract()[0]
            performance['Tm'] = p.xpath('.//*[@data-stat="team_id"]/a/text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="team_id"]/a/text()').extract()) > 0 \
                else p.xpath('.//*[@data-stat="team_id"]/text()').extract()[0]
            performance['Lg'] = self.fun(p, './/*[@data-stat="lg_id"]/a/text()')
            performance['Pos'] = self.fun(p, './/*[@data-stat="pos"]/text()')
            performance['G'] = self.fun(p, './/*[@data-stat="g"]//text()')
            performance['MP'] = self.fun(p, './/*[@data-stat="mp"]//text()')
            performance['PER'] = self.fun(p, './/*[@data-stat="per"]//text()')
            performance['TS%'] = self.fun(p, './/*[@data-stat="ts_pct"]//text()')
            performance['3PAr'] = self.fun(p, './/*[@data-stat="fg3a_per_fga_pct"]//text()')
            performance['FTr'] = self.fun(p, './/*[@data-stat="fta_per_fga_pct"]//text()')
            performance['ORB%'] = self.fun(p, './/*[@data-stat="orb_pct"]//text()')
            performance['DRB%'] = self.fun(p, './/*[@data-stat="drb_pct"]//text()')
            performance['TRB%'] = self.fun(p, './/*[@data-stat="trb_pct"]//text()')
            performance['AST%'] = self.fun(p, './/*[@data-stat="ast_pct"]//text()')
            performance['STL%'] = self.fun(p, './/*[@data-stat="stl_pct"]//text()')
            performance['BLK%'] = self.fun(p, './/*[@data-stat="blk_pct"]//text()')
            performance['TOV%'] = self.fun(p, './/*[@data-stat="tov_pct"]//text()')
            performance['USG%'] = self.fun(p, './/*[@data-stat="usg_pct"]//text()')
            performance['OWS'] = self.fun(p, './/*[@data-stat="ows"]//text()')

            performance['DWS'] = self.fun(p, './/*[@data-stat="dws"]//text()')
            performance['WS'] = self.fun(p, './/*[@data-stat="ws"]//text()')
            performance['WS/48'] = self.fun(p, './/*[@data-stat="ws_per_48"]//text()')
            performance['OBPM'] = self.fun(p, './/*[@data-stat="obpm"]//text()')
            performance['DBPM'] = self.fun(p, './/*[@data-stat="dbpm"]//text()')
            performance['BPM'] = self.fun(p, './/*[@data-stat="bpm"]//text()')
            performance['VORP'] = self.fun(p, './/*[@data-stat="vorp"]//text()')

            #print(performance)
            yield performance

        for p in response.xpath('.//tr[starts-with(@id, "playoffs_advanced")]'):
            # print(p.extract())
            performance = {}
            performance['Name'] = name
            performance['Born'] = born
            performance['Is_playoff'] = '1'
            performance['Season'] = p.xpath('.//*[@data-stat="season"]/a/text()').extract()[0]
            if int(performance['Season'].split('-')[0]) > 2020 or int(performance['Season'].split('-')[0]) < 2009:
                continue
            performance['Age'] = p.xpath('.//*[@data-stat="age"]/text()').extract()[0]
            performance['Tm'] = p.xpath('.//*[@data-stat="team_id"]/a/text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="team_id"]/a/text()').extract()) > 0 \
                else p.xpath('.//*[@data-stat="team_id"]/text()').extract()[0]
            performance['Lg'] = self.fun(p, './/*[@data-stat="lg_id"]/a/text()')
            performance['Pos'] = self.fun(p, './/*[@data-stat="pos"]/text()')
            performance['G'] = self.fun(p, './/*[@data-stat="g"]//text()')
            performance['MP'] = self.fun(p, './/*[@data-stat="mp"]//text()')
            performance['PER'] = self.fun(p, './/*[@data-stat="per"]//text()')
            performance['TS%'] = self.fun(p, './/*[@data-stat="ts_pct"]//text()')
            performance['3PAr'] = self.fun(p, './/*[@data-stat="fg3a_per_fga_pct"]//text()')
            performance['FTr'] = self.fun(p, './/*[@data-stat="fta_per_fga_pct"]//text()')
            performance['ORB%'] = self.fun(p, './/*[@data-stat="orb_pct"]//text()')
            performance['DRB%'] = self.fun(p, './/*[@data-stat="drb_pct"]//text()')
            performance['TRB%'] = self.fun(p, './/*[@data-stat="trb_pct"]//text()')
            performance['AST%'] = self.fun(p, './/*[@data-stat="ast_pct"]//text()')
            performance['STL%'] = self.fun(p, './/*[@data-stat="stl_pct"]//text()')
            performance['BLK%'] = self.fun(p, './/*[@data-stat="blk_pct"]//text()')
            performance['TOV%'] = self.fun(p, './/*[@data-stat="tov_pct"]//text()')
            performance['USG%'] = self.fun(p, './/*[@data-stat="usg_pct"]//text()')
            performance['OWS'] = self.fun(p, './/*[@data-stat="ows"]//text()')

            performance['DWS'] = self.fun(p, './/*[@data-stat="dws"]//text()')
            performance['WS'] = self.fun(p, './/*[@data-stat="ws"]//text()')
            performance['WS/48'] = self.fun(p, './/*[@data-stat="ws_per_48"]//text()')
            performance['OBPM'] = self.fun(p, './/*[@data-stat="obpm"]//text()')
            performance['DBPM'] = self.fun(p, './/*[@data-stat="dbpm"]//text()')
            performance['BPM'] = self.fun(p, './/*[@data-stat="bpm"]//text()')
            performance['VORP'] = self.fun(p, './/*[@data-stat="vorp"]//text()')

            # print(performance)
            yield performance

    def fun(self, p, pattern):
        return p.xpath(pattern).extract()[0] if len(p.xpath(pattern).extract()) > 0 else ''
