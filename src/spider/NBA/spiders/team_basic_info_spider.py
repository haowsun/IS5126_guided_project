import scrapy
import re

class NBATeamBISpider(scrapy.Spider):
    name = "nba_team_basic_info"
    start_urls = ['https://www.basketball-reference.com/teams/']

    def parse(self, response):
        teams_table = response.css('table#teams_active tbody tr')
        for team in teams_table:
            team_page = team.css('th a::attr(href)').get()
            if team_page is not None:
                yield response.follow(team_page, callback=self.parse_team_page)
    def parse_team_page(self, response):
        basic_info = response.css('div#meta div')[1]
        yield{
            'name': basic_info.css('h1 span::text').get().replace('\n', '').strip(' '),
            'location': basic_info.css('p ::text')[2].get().replace('\n', '').strip(' '),
            'Team Names': basic_info.css('p ::text')[5].get().replace('\n', '').strip(' '),
            'seasons played': basic_info.css('p ::text')[8].get().replace('\n', '').strip(' '),
            'record': basic_info.css('p ::text')[11].get().replace('\n', '').strip(' '),
            'playoff appearance': basic_info.css('p ::text')[14].get().replace('\n', '').strip(' '),
            'championship': basic_info.css('p ::text')[17].get().replace('\n', '').strip(' ')
        }