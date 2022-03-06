# -*-coding:utf-8-*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import string
import re
from items import *
from scrapy.selector import Selector


class pbp_spider(scrapy.Spider):
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


        table = response.xpath('//*[starts-with(@id, "all_pbp-playoffs_pbp")]').extract()[0] \
            if len(response.xpath('//*[starts-with(@id, "all_pbp-playoffs_pbp")]').extract()) > 0 else ''
        table = re.sub('<!--', '', table)
        table = re.sub('-->', '', table)
        table = Selector(text=table)

        for p in table.xpath('.//tr[starts-with(@id, "pbp")]'):
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
            performance['PG%'] = self.fun(p, './/*[@data-stat="pct_1"]//text()')
            performance['SG%'] = self.fun(p, './/*[@data-stat="pct_2"]//text()')
            performance['SF%'] = self.fun(p, './/*[@data-stat="pct_3"]//text()')
            performance['PF%'] = self.fun(p, './/*[@data-stat="pct_4"]//text()')
            performance['C%'] = self.fun(p, './/*[@data-stat="pct_5"]//text()')
            performance['OnCount'] = self.fun(p, './/*[@data-stat="plus_minus_on"]//text()')
            performance['On-Off'] = self.fun(p, './/*[@data-stat="plus_minus_net"]//text()')
            performance['BadPass'] = self.fun(p, './/*[@data-stat="tov_bad_pass"]//text()')
            performance['LostBall'] = self.fun(p, './/*[@data-stat="tov_lost_ball"]//text()')
            performance['FoulShooting'] = self.fun(p, './/*[@data-stat="fouls_shooting"]//text()')
            performance['FoulOffensive'] = self.fun(p, './/*[@data-stat="fouls_offensive"]//text()')
            performance['DrawnShooting'] = self.fun(p, './/*[@data-stat="drawn_shooting"]//text()')
            performance['DrawnOffensive'] = self.fun(p, './/*[@data-stat="drawn_offensive"]//text()')
            performance['PGA'] = self.fun(p, './/*[@data-stat="astd_pts"]//text()')
            performance['And1'] = self.fun(p, './/*[@data-stat="and1s"]//text()')
            performance['Blkd'] = self.fun(p, './/*[@data-stat="own_shots_blk"]//text()')

            #print(performance)
            yield performance

        for p in table.xpath('.//tr[starts-with(@id, "playoffs_pbp")]'):
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
            performance['PG%'] = self.fun(p, './/*[@data-stat="pct_1"]//text()')
            performance['SG%'] = self.fun(p, './/*[@data-stat="pct_2"]//text()')
            performance['SF%'] = self.fun(p, './/*[@data-stat="pct_3"]//text()')
            performance['PF%'] = self.fun(p, './/*[@data-stat="pct_4"]//text()')
            performance['C%'] = self.fun(p, './/*[@data-stat="pct_5"]//text()')
            performance['OnCount'] = self.fun(p, './/*[@data-stat="plus_minus_on"]//text()')
            performance['On-Off'] = self.fun(p, './/*[@data-stat="plus_minus_net"]//text()')
            performance['BadPass'] = self.fun(p, './/*[@data-stat="tov_bad_pass"]//text()')
            performance['LostBall'] = self.fun(p, './/*[@data-stat="tov_lost_ball"]//text()')
            performance['FoulShooting'] = self.fun(p, './/*[@data-stat="fouls_shooting"]//text()')
            performance['FoulOffensive'] = self.fun(p, './/*[@data-stat="fouls_offensive"]//text()')
            performance['DrawnShooting'] = self.fun(p, './/*[@data-stat="drawn_shooting"]//text()')
            performance['DrawnOffensive'] = self.fun(p, './/*[@data-stat="drawn_offensive"]//text()')
            performance['PGA'] = self.fun(p, './/*[@data-stat="astd_pts"]//text()')
            performance['And1'] = self.fun(p, './/*[@data-stat="and1s"]//text()')
            performance['Blkd'] = self.fun(p, './/*[@data-stat="own_shots_blk"]//text()')

            # print(performance)
            yield performance

    def fun(self, p, pattern):
        return p.xpath(pattern).extract()[0] if len(p.xpath(pattern).extract()) > 0 else ''
