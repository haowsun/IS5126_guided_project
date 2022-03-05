# -*-coding:utf-8-*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import string
import re
from items import *
from scrapy.selector import Selector


class shooting_spider(scrapy.Spider):
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


        table = response.xpath('//*[starts-with(@id, "all_shooting-playoffs_shooting")]').extract()[0] \
            if len(response.xpath('//*[starts-with(@id, "all_shooting-playoffs_shooting")]').extract()) > 0 else ''
        table = re.sub('<!--', '', table)
        table = re.sub('-->', '', table)
        table = Selector(text=table)

        for p in table.xpath('.//tr[starts-with(@id, "shooting")]'):
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
            performance['FG%'] = self.fun(p, './/*[@data-stat="fg_pct"]//text()')
            performance['Dist'] = self.fun(p, './/*[@data-stat="avg_dist"]//text()')
            performance['2P_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_fg2a"]//text()')
            performance['0-3_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_00_03"]//text()')
            performance['3-10_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_03_10"]//text()')
            performance['10-16_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_10_16"]//text()')
            performance['16-3P_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_16_xx"]//text()')
            performance['3P_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_fg3a"]//text()')
            performance['2P_FG'] = self.fun(p, './/*[@data-stat="fg_pct_fg2a"]//text()')
            performance['0-3_FG'] = self.fun(p, './/*[@data-stat="fg_pct_00_03"]//text()')
            performance['3-10_FG'] = self.fun(p, './/*[@data-stat="fg_pct_03_10"]//text()')
            performance['10-16_FG'] = self.fun(p, './/*[@data-stat="fg_pct_10_16"]//text()')
            performance['16-3P_FG'] = self.fun(p, './/*[@data-stat="fg_pct_16_xx"]//text()')
            performance['3P_FG'] = self.fun(p, './/*[@data-stat="fg_pct_fg3a"]//text()')
            performance['2P_AST'] = self.fun(p, './/*[@data-stat="pct_ast_fg2"]//text()')
            performance['3P_AST'] = self.fun(p, './/*[@data-stat="pct_ast_fg3"]//text()')
            performance['FGA_DUNK'] = self.fun(p, './/*[@data-stat="pct_fga_dunk"]//text()')
            performance['FG_DUNK'] = self.fun(p, './/*[@data-stat="fg_dunk"]//text()')
            performance['FG3A_Corner3'] = self.fun(p, './/*[@data-stat="pct_fg3a_corner3"]//text()')
            performance['FG_Corner3'] = self.fun(p, './/*[@data-stat="fg_pct_corner3"]//text()')
            performance['FG3A_Heave'] = self.fun(p, './/*[@data-stat="fg3a_heave"]//text()')
            performance['FG3_heave'] = self.fun(p, './/*[@data-stat="fg3_heave"]//text()')

            #print(performance)
            yield performance

        for p in table.xpath('.//tr[starts-with(@id, "playoffs_shooting")]'):
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
            performance['FG%'] = self.fun(p, './/*[@data-stat="fg_pct"]//text()')
            performance['Dist'] = self.fun(p, './/*[@data-stat="avg_dist"]//text()')
            performance['2P_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_fg2a"]//text()')
            performance['0-3_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_00_03"]//text()')
            performance['3-10_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_03_10"]//text()')
            performance['10-16_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_10_16"]//text()')
            performance['16-3P_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_16_xx"]//text()')
            performance['3P_FGA'] = self.fun(p, './/*[@data-stat="pct_fga_fg3a"]//text()')
            performance['2P_FG'] = self.fun(p, './/*[@data-stat="fg_pct_fg2a"]//text()')
            performance['0-3_FG'] = self.fun(p, './/*[@data-stat="fg_pct_00_03"]//text()')
            performance['3-10_FG'] = self.fun(p, './/*[@data-stat="fg_pct_03_10"]//text()')
            performance['10-16_FG'] = self.fun(p, './/*[@data-stat="fg_pct_10_16"]//text()')
            performance['16-3P_FG'] = self.fun(p, './/*[@data-stat="fg_pct_16_xx"]//text()')
            performance['3P_FG'] = self.fun(p, './/*[@data-stat="fg_pct_fg3a"]//text()')
            performance['2P_AST'] = self.fun(p, './/*[@data-stat="pct_ast_fg2"]//text()')
            performance['3P_AST'] = self.fun(p, './/*[@data-stat="pct_ast_fg3"]//text()')
            performance['FGA_DUNK'] = self.fun(p, './/*[@data-stat="pct_fga_dunk"]//text()')
            performance['FG_DUNK'] = self.fun(p, './/*[@data-stat="fg_dunk"]//text()')
            performance['FG3A_Corner3'] = self.fun(p, './/*[@data-stat="pct_fg3a_corner3"]//text()')
            performance['FG_Corner3'] = self.fun(p, './/*[@data-stat="fg_pct_corner3"]//text()')
            performance['FG3A_Heave'] = self.fun(p, './/*[@data-stat="fg3a_heave"]//text()')
            performance['FG3_heave'] = self.fun(p, './/*[@data-stat="fg3_heave"]//text()')

            # print(performance)
            yield performance

    def fun(self, p, pattern):
        return p.xpath(pattern).extract()[0] if len(p.xpath(pattern).extract()) > 0 else ''
