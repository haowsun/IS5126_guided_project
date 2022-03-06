# -*-coding:utf-8-*-
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import string
import re
from items import *


class nba_spider(scrapy.Spider):
    name = "nba"
    start_urls = ['https://www.basketball-reference.com/players/' + x + '/' for x in string.ascii_lowercase]

    def parse(self, response, *args, **kwargs):
        for player in response.xpath('//*[@id="players"]/tbody//tr'):
            link = player.xpath('./th//a/@href')[0]
            begin_year = player.xpath('.//*[@data-stat="year_min"]/text()').extract()[0]
            end_year = player.xpath('.//*[@data-stat="year_max"]/text()').extract()[0]

            if int(end_year) >= 2009:
                yield response.follow(link, self.parse_player)

    def parse_player(self, response):
        playerItem = {}
        print(response)
        playerItem['Name'] = response.xpath('//*[@itemprop="name"]/span/text()').extract()[0]

        playerItem['Position'] = \
            response.xpath('//strong[contains(text(), "Position:")]/following-sibling::text()').extract()[0].strip() \
                if len(response.xpath('//strong[contains(text(), "Position:")]/following-sibling::text()').extract()) > 0 else ''

        playerItem['Position'] = re.sub(r'\s+', ' ', str(playerItem['Position'])) + ' Shoots: '
        s = response.xpath('//strong[contains(text(), "Shoots:")]/following-sibling::text()').extract()[0].strip() \
            if len(response.xpath('//strong[contains(text(), "Shoots:")]/following-sibling::text()').extract()) > 0 else ''
        s = re.sub(r'\s+', ' ', str(s))
        playerItem['Position'] += s

        playerItem['Height'] = response.xpath('//*[@itemprop="height"]/text()').extract()[0] \
            if len(response.xpath('//*[@itemprop="height"]/text()').extract()) > 0 else ''

        playerItem['Weight'] = response.xpath('//*[@itemprop="weight"]/text()').extract()[0] \
            if len(response.xpath('//*[@itemprop="weight"]/text()').extract()) > 0 else ''

        playerItem['Born'] = response.xpath('//*[@itemprop="birthDate"]/@data-birth').extract()[0] \
            if len(response.xpath('//*[@itemprop="birthDate"]/@data-birth').extract()) > 0 else ''

        playerItem['Recruiting_rank'] = response.xpath('//strong[contains(text(), "Recruiting")]/following-sibling::*/text()').extract()[0] \
            if len(response.xpath('//strong[contains(text(), "Recruiting")]/following-sibling::*/text()').extract()) > 0 else ''
        if len(playerItem['Recruiting_rank']) > 0:
            playerItem['Recruiting_rank'] += ' ' + response.xpath('//strong[contains(text(), "Recruiting Rank:")]/following-sibling::text()[2]').extract()[0].strip()

        playerItem['Draft_team'] = \
        response.xpath('//strong[contains(text(), "Draft:")]/following-sibling::*/text()').extract()[0] \
            if len(response.xpath('//strong[contains(text(), "Draft:")]/following-sibling::*/text()').extract()) > 0 else ''

        playerItem['Experience'] = response.xpath('//strong[contains(text(), "Experience:")]/following-sibling::text()').extract()[0].strip() \
            if len(response.xpath('//strong[contains(text(), "Experience:")]/following-sibling::text()').extract()) > 0 else ''

        playerItem['Career_length'] = response.xpath('//strong[contains(text(), "Career Length:")]/following-sibling::text()').extract()[0].strip() \
            if len(response.xpath('//strong[contains(text(), "Career Length:")]/following-sibling::text()').extract()) > 0 else ''

        print(playerItem)
        yield playerItem
