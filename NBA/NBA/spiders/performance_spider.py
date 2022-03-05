# -*-coding:utf-8-*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import string
import re
from items import *


class performance_spider(scrapy.Spider):
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

        for p in response.xpath('//tr[starts-with(@id, "per_game")]'):
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
            performance['Lg'] = p.xpath('.//*[@data-stat="lg_id"]/a/text()').extract()[0]
            performance['Pos'] = p.xpath('.//*[@data-stat="pos"]/text()').extract()[0]
            performance['G'] = p.xpath('.//*[@data-stat="g"]//text()').extract()[0]
            performance['GS'] = p.xpath('.//*[@data-stat="gs"]//text()').extract()[0]
            performance['MP'] = p.xpath('.//*[@data-stat="mp_per_g"]//text()').extract()[0]
            performance['FG'] = p.xpath('.//*[@data-stat="fg_per_g"]//text()').extract()[0]
            performance['FGA'] = p.xpath('.//*[@data-stat="fga_per_g"]//text()').extract()[0]
            performance['FG%'] = p.xpath('.//*[@data-stat="fg_pct"]//text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="fg_pct"]//text()').extract()) > 0 else ''
            performance['3P'] = p.xpath('.//*[@data-stat="fg3_per_g"]//text()').extract()[0]
            performance['3PA'] = p.xpath('.//*[@data-stat="fg3a_per_g"]//text()').extract()[0]
            performance['3P%'] = p.xpath('.//*[@data-stat="fg3_pct"]//text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="fg3_pct"]//text()').extract()) > 0 else ''
            performance['2P'] = p.xpath('.//*[@data-stat="fg2_per_g"]//text()').extract()[0]
            performance['2PA'] = p.xpath('.//*[@data-stat="fg2a_per_g"]//text()').extract()[0]
            performance['2P%'] = p.xpath('.//*[@data-stat="fg2_pct"]//text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="fg2_pct"]//text()').extract()) > 0 else ''
            performance['eFG%'] = p.xpath('.//*[@data-stat="efg_pct"]//text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="efg_pct"]//text()').extract()) > 0 else ''
            performance['FT'] = p.xpath('.//*[@data-stat="ft_per_g"]//text()').extract()[0]
            performance['FTA'] = p.xpath('.//*[@data-stat="fta_per_g"]//text()').extract()[0]
            performance['FT%'] = p.xpath('.//*[@data-stat="ft_pct"]//text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="ft_pct"]//text()').extract()) > 0 else ''

            performance['ORB'] = p.xpath('.//*[@data-stat="orb_per_g"]//text()').extract()[0]
            performance['DRB'] = p.xpath('.//*[@data-stat="drb_per_g"]//text()').extract()[0]
            performance['TRB'] = p.xpath('.//*[@data-stat="trb_per_g"]//text()').extract()[0]
            performance['AST'] = p.xpath('.//*[@data-stat="ast_per_g"]//text()').extract()[0]
            performance['STL'] = p.xpath('.//*[@data-stat="stl_per_g"]//text()').extract()[0]
            performance['BLK'] = p.xpath('.//*[@data-stat="blk_per_g"]//text()').extract()[0]
            performance['TOV'] = p.xpath('.//*[@data-stat="tov_per_g"]//text()').extract()[0]
            performance['PF'] = p.xpath('.//*[@data-stat="pf_per_g"]//text()').extract()[0]
            performance['PTS'] = p.xpath('.//*[@data-stat="pts_per_g"]//text()').extract()[0]

            #print(performance)
            yield performance

        for p in response.xpath('//tr[starts-with(@id, "playoffs_per_game")]'):
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
            performance['Lg'] = p.xpath('.//*[@data-stat="lg_id"]/a/text()').extract()[0]
            performance['Pos'] = p.xpath('.//*[@data-stat="pos"]/text()').extract()[0]
            performance['G'] = p.xpath('.//*[@data-stat="g"]//text()').extract()[0]
            performance['GS'] = p.xpath('.//*[@data-stat="gs"]//text()').extract()[0]
            performance['MP'] = p.xpath('.//*[@data-stat="mp_per_g"]//text()').extract()[0]
            performance['FG'] = p.xpath('.//*[@data-stat="fg_per_g"]//text()').extract()[0]
            performance['FGA'] = p.xpath('.//*[@data-stat="fga_per_g"]//text()').extract()[0]
            performance['FG%'] = p.xpath('.//*[@data-stat="fg_pct"]//text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="fg_pct"]//text()').extract()) > 0 else ''
            performance['3P'] = p.xpath('.//*[@data-stat="fg3_per_g"]//text()').extract()[0]
            performance['3PA'] = p.xpath('.//*[@data-stat="fg3a_per_g"]//text()').extract()[0]
            performance['3P%'] = p.xpath('.//*[@data-stat="fg3_pct"]//text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="fg3_pct"]//text()').extract()) > 0 else ''
            performance['2P'] = p.xpath('.//*[@data-stat="fg2_per_g"]//text()').extract()[0]
            performance['2PA'] = p.xpath('.//*[@data-stat="fg2a_per_g"]//text()').extract()[0]
            performance['2P%'] = p.xpath('.//*[@data-stat="fg2_pct"]//text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="fg2_pct"]//text()').extract()) > 0 else ''
            performance['eFG%'] = p.xpath('.//*[@data-stat="efg_pct"]//text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="efg_pct"]//text()').extract()) > 0 else ''
            performance['FT'] = p.xpath('.//*[@data-stat="ft_per_g"]//text()').extract()[0]
            performance['FTA'] = p.xpath('.//*[@data-stat="fta_per_g"]//text()').extract()[0]
            performance['FT%'] = p.xpath('.//*[@data-stat="ft_pct"]//text()').extract()[0] \
                if len(p.xpath('.//*[@data-stat="ft_pct"]//text()').extract()) > 0 else ''

            performance['ORB'] = p.xpath('.//*[@data-stat="orb_per_g"]//text()').extract()[0]
            performance['DRB'] = p.xpath('.//*[@data-stat="drb_per_g"]//text()').extract()[0]
            performance['TRB'] = p.xpath('.//*[@data-stat="trb_per_g"]//text()').extract()[0]
            performance['AST'] = p.xpath('.//*[@data-stat="ast_per_g"]//text()').extract()[0]
            performance['STL'] = p.xpath('.//*[@data-stat="stl_per_g"]//text()').extract()[0]
            performance['BLK'] = p.xpath('.//*[@data-stat="blk_per_g"]//text()').extract()[0]
            performance['TOV'] = p.xpath('.//*[@data-stat="tov_per_g"]//text()').extract()[0]
            performance['PF'] = p.xpath('.//*[@data-stat="pf_per_g"]//text()').extract()[0]
            performance['PTS'] = p.xpath('.//*[@data-stat="pts_per_g"]//text()').extract()[0]

            # print(performance)
            yield performance