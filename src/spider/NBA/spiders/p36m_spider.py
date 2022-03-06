# -*-coding:utf-8-*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import string
import re
from items import *
from scrapy.selector import Selector


class p36m_spider(scrapy.Spider):
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

        table = response.xpath('//*[starts-with(@id, "all_per_minute")]').extract()[0] \
            if len(response.xpath('//*[starts-with(@id, "all_per_minute")]').extract()) > 0 else ''
        table = re.sub('<!--', '', table)
        table = re.sub('-->', '', table)
        table = Selector(text=table)

        for p in table.xpath('.//tr[starts-with(@id, "per_minute")]'):
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
            performance['GS'] = self.fun(p, './/*[@data-stat="gs"]//text()')
            performance['MP'] = self.fun(p, './/*[@data-stat="mp"]//text()')
            performance['FG'] = self.fun(p, './/*[@data-stat="fg_per_mp"]//text()')
            performance['FGA'] = self.fun(p, './/*[@data-stat="fga_per_mp"]//text()')
            performance['FG%'] = self.fun(p, './/*[@data-stat="fg_pct"]//text()')
            performance['3P'] = self.fun(p, './/*[@data-stat="fg3_per_mp"]//text()')
            performance['3PA'] = self.fun(p, './/*[@data-stat="fg3a_per_mp"]//text()')
            performance['3P%'] = self.fun(p, './/*[@data-stat="fg3_pct"]//text()')
            performance['2P'] = self.fun(p, './/*[@data-stat="fg2_per_mp"]//text()')
            performance['2PA'] = self.fun(p, './/*[@data-stat="fg2a_per_mp"]//text()')
            performance['2P%'] = self.fun(p, './/*[@data-stat="fg2_pct"]//text()')
            performance['FT'] = self.fun(p, './/*[@data-stat="ft_per_mp"]//text()')
            performance['FTA'] = self.fun(p, './/*[@data-stat="fta_per_mp"]//text()')
            performance['FT%'] = self.fun(p, './/*[@data-stat="ft_pct"]//text()')

            performance['ORB'] = self.fun(p, './/*[@data-stat="orb_per_mp"]//text()')
            performance['DRB'] = self.fun(p, './/*[@data-stat="drb_per_mp"]//text()')
            performance['TRB'] = self.fun(p, './/*[@data-stat="trb_per_mp"]//text()')
            performance['AST'] = self.fun(p, './/*[@data-stat="ast_per_mp"]//text()')
            performance['STL'] = self.fun(p, './/*[@data-stat="stl_per_mp"]//text()')
            performance['BLK'] = self.fun(p, './/*[@data-stat="blk_per_mp"]//text()')
            performance['TOV'] = self.fun(p, './/*[@data-stat="tov_per_mp"]//text()')
            performance['PF'] = self.fun(p, './/*[@data-stat="pf_per_mp"]//text()')
            performance['PTS'] = self.fun(p, './/*[@data-stat="pts_per_mp"]//text()')

            #print(performance)
            yield performance

        for p in table.xpath('.//tr[starts-with(@id, "playoffs_per_minute")]'):
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
            performance['GS'] = self.fun(p, './/*[@data-stat="gs"]//text()')
            performance['MP'] = self.fun(p, './/*[@data-stat="mp"]//text()')
            performance['FG'] = self.fun(p, './/*[@data-stat="fg_per_mp"]//text()')
            performance['FGA'] = self.fun(p, './/*[@data-stat="fga_per_mp"]//text()')
            performance['FG%'] = self.fun(p, './/*[@data-stat="fg_pct"]//text()')
            performance['3P'] = self.fun(p, './/*[@data-stat="fg3_per_mp"]//text()')
            performance['3PA'] = self.fun(p, './/*[@data-stat="fg3a_per_mp"]//text()')
            performance['3P%'] = self.fun(p, './/*[@data-stat="fg3_pct"]//text()')
            performance['2P'] = self.fun(p, './/*[@data-stat="fg2_per_mp"]//text()')
            performance['2PA'] = self.fun(p, './/*[@data-stat="fg2a_per_mp"]//text()')
            performance['2P%'] = self.fun(p, './/*[@data-stat="fg2_pct"]//text()')
            performance['FT'] = self.fun(p, './/*[@data-stat="ft_per_mp"]//text()')
            performance['FTA'] = self.fun(p, './/*[@data-stat="fta_per_mp"]//text()')
            performance['FT%'] = self.fun(p, './/*[@data-stat="ft_pct"]//text()')

            performance['ORB'] = self.fun(p, './/*[@data-stat="orb_per_mp"]//text()')
            performance['DRB'] = self.fun(p, './/*[@data-stat="drb_per_mp"]//text()')
            performance['TRB'] = self.fun(p, './/*[@data-stat="trb_per_mp"]//text()')
            performance['AST'] = self.fun(p, './/*[@data-stat="ast_per_mp"]//text()')
            performance['STL'] = self.fun(p, './/*[@data-stat="stl_per_mp"]//text()')
            performance['BLK'] = self.fun(p, './/*[@data-stat="blk_per_mp"]//text()')
            performance['TOV'] = self.fun(p, './/*[@data-stat="tov_per_mp"]//text()')
            performance['PF'] = self.fun(p, './/*[@data-stat="pf_per_mp"]//text()')
            performance['PTS'] = self.fun(p, './/*[@data-stat="pts_per_mp"]//text()')

            # print(performance)
            yield performance

    def fun(self, p, pattern):
        return p.xpath(pattern).extract()[0] if len(p.xpath(pattern).extract()) > 0 else ''
