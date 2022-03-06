# -*-coding:utf-8-*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import string
import re
from items import *
from scrapy.selector import Selector


class adjusted_spider(scrapy.Spider):
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

        table = response.xpath('//*[starts-with(@id, "all_adj_shooting")]').extract()[0] \
            if len(response.xpath('//*[starts-with(@id, "all_adj_shooting")]').extract()) > 0 else ''
        table = re.sub('<!--', '', table)
        table = re.sub('-->', '', table)
        table = Selector(text=table)

        for p in table.xpath('.//tr[starts-with(@id, "adj_shooting")]'):
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
            performance['FG'] = self.fun(p, './/*[@data-stat="fg_pct"]//text()')
            performance['2P'] = self.fun(p, './/*[@data-stat="fg2_pct"]//text()')
            performance['3P'] = self.fun(p, './/*[@data-stat="fg3_pct"]//text()')
            performance['eFG'] = self.fun(p, './/*[@data-stat="efg_pct"]//text()')
            performance['FT'] = self.fun(p, './/*[@data-stat="ft_pct"]//text()')
            performance['TS'] = self.fun(p, './/*[@data-stat="ts_pct"]//text()')
            performance['FTr'] = self.fun(p, './/*[@data-stat="fta_per_fga_pct"]//text()')
            performance['3PAr'] = self.fun(p, './/*[@data-stat="fg3a_per_fga_pct"]//text()')
            performance['L_FG'] = self.fun(p, './/*[@data-stat="lg_fg_pct"]//text()')
            performance['L_2P'] = self.fun(p, './/*[@data-stat="lg_fg2_pct"]//text()')
            performance['L_3P'] = self.fun(p, './/*[@data-stat="lg_fg3_pct"]//text()')
            performance['L_eFG'] = self.fun(p, './/*[@data-stat="lg_efg_pct"]//text()')
            performance['L_FT'] = self.fun(p, './/*[@data-stat="lg_ft_pct"]//text()')
            performance['L_TS'] = self.fun(p, './/*[@data-stat="lg_ts_pct"]//text()')
            performance['L_FTr'] = self.fun(p, './/*[@data-stat="lg_fta_per_fga_pct"]//text()')
            performance['L_3PAr'] = self.fun(p, './/*[@data-stat="lg_fg3a_per_fga_pct"]//text()')
            performance['FG+'] = self.fun(p, './/*[@data-stat="adj_fg_pct"]//text()')
            performance['2P+'] = self.fun(p, './/*[@data-stat="adj_fg2_pct"]//text()')
            performance['3P+'] = self.fun(p, './/*[@data-stat="adj_fg3_pct"]//text()')
            performance['eFG+'] = self.fun(p, './/*[@data-stat="adj_efg_pct"]//text()')
            performance['FT+'] = self.fun(p, './/*[@data-stat="adj_ft_pct"]//text()')
            performance['TS+'] = self.fun(p, './/*[@data-stat="adj_ts_pct"]//text()')
            performance['FTr+'] = self.fun(p, './/*[@data-stat="adj_fta_per_fga_pct"]//text()')
            performance['3PAr+'] = self.fun(p, './/*[@data-stat="adj_fg3a_per_fga_pct"]//text()')
            performance['FG_Add'] = self.fun(p, './/*[@data-stat="fg_pts_added"]//text()')
            performance['TS_Add'] = self.fun(p, './/*[@data-stat="ts_pts_added"]//text()')

            #print(performance)
            yield performance

        for p in table.xpath('.//tr[starts-with(@id, "playoffs_adj_shooting")]'):
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
            performance['FG'] = self.fun(p, './/*[@data-stat="fg_pct"]//text()')
            performance['2P'] = self.fun(p, './/*[@data-stat="fg2_pct"]//text()')
            performance['3P'] = self.fun(p, './/*[@data-stat="fg3_pct"]//text()')
            performance['eFG'] = self.fun(p, './/*[@data-stat="efg_pct"]//text()')
            performance['FT'] = self.fun(p, './/*[@data-stat="ft_pct"]//text()')
            performance['TS'] = self.fun(p, './/*[@data-stat="ts_pct"]//text()')
            performance['FTr'] = self.fun(p, './/*[@data-stat="fta_per_fga_pct"]//text()')
            performance['3PAr'] = self.fun(p, './/*[@data-stat="fg3a_per_fga_pct"]//text()')
            performance['L_FG'] = self.fun(p, './/*[@data-stat="lg_fg_pct"]//text()')
            performance['L_2P'] = self.fun(p, './/*[@data-stat="lg_fg2_pct"]//text()')
            performance['L_3P'] = self.fun(p, './/*[@data-stat="lg_fg3_pct"]//text()')
            performance['L_eFG'] = self.fun(p, './/*[@data-stat="lg_efg_pct"]//text()')
            performance['L_FT'] = self.fun(p, './/*[@data-stat="lg_ft_pct"]//text()')
            performance['L_TS'] = self.fun(p, './/*[@data-stat="lg_ts_pct"]//text()')
            performance['L_FTr'] = self.fun(p, './/*[@data-stat="lg_fta_per_fga_pct"]//text()')
            performance['L_3PAr'] = self.fun(p, './/*[@data-stat="lg_fg3a_per_fga_pct"]//text()')
            performance['FG+'] = self.fun(p, './/*[@data-stat="adj_fg_pct"]//text()')
            performance['2P+'] = self.fun(p, './/*[@data-stat="adj_fg2_pct"]//text()')
            performance['3P+'] = self.fun(p, './/*[@data-stat="adj_fg3_pct"]//text()')
            performance['eFG+'] = self.fun(p, './/*[@data-stat="adj_efg_pct"]//text()')
            performance['FT+'] = self.fun(p, './/*[@data-stat="adj_ft_pct"]//text()')
            performance['TS+'] = self.fun(p, './/*[@data-stat="adj_ts_pct"]//text()')
            performance['FTr+'] = self.fun(p, './/*[@data-stat="adj_fta_per_fga_pct"]//text()')
            performance['3PAr+'] = self.fun(p, './/*[@data-stat="adj_fg3a_per_fga_pct"]//text()')
            performance['FG_Add'] = self.fun(p, './/*[@data-stat="fg_pts_added"]//text()')
            performance['TS_Add'] = self.fun(p, './/*[@data-stat="ts_pts_added"]//text()')

            # print(performance)
            yield performance

    def fun(self, p, pattern):
        return p.xpath(pattern).extract()[0] if len(p.xpath(pattern).extract()) > 0 else ''
