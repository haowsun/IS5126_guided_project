import scrapy
import re

class NBATeamSSBasicSpider(scrapy.Spider):
    name = "nba_team_seasional_basic_stats"
    start_urls = ['https://www.basketball-reference.com/teams/']

    def parse(self, response):
        teams_table = response.css('table#teams_active tbody tr')
        for team in teams_table:
            team_page = team.css('th a::attr(href)').get()
            if team_page is not None:
                yield response.follow(team_page, callback=self.parse_team_page)

    def parse_team_page(self, response):
        bot_nav = response.css('div#bottom_nav_container')
        basic_stats_page = bot_nav.css('a::attr(href)')[1].get()
        if basic_stats_page is not None:
            yield response.follow(basic_stats_page, callback=self.parse_team_page_basic_stats)

    def parse_team_page_basic_stats(self, response):
        pattern_season_range = '^20(0[9]|1[0-9]|2[0])'
        stats_all_seasons = response.css('table.sortable.stats_table tbody tr')
        for stats_season in stats_all_seasons:
            season = stats_season.css('th ::text').get()
            Lg = stats_season.css('td[data-stat="lg_id"] ::text').get()
            if re.match(pattern_season_range, season) is not None and Lg == 'NBA':
                yield{
                    'name': response.css('div#meta div')[1].css('h1 span::text').get().replace('\n', '').strip(' '),
                    'Season': season,
                    'Lg': Lg,
                    'Tm': stats_season.css('td[data-stat="team_id"] ::text').get(),
                    'W': stats_season.css('td[data-stat="wins"] ::text').get(),
                    'L': stats_season.css('td[data-stat="losses"] ::text').get(),
                    'Finish': stats_season.css('td[data-stat="rank_team"] ::text').get(),
                    'Age': stats_season.css('td[data-stat="avg_age"] ::text').get(),
                    'Ht.': stats_season.css('td[data-stat="avg_ht"] ::text').get(),
                    'Wt.': stats_season.css('td[data-stat="avg_wt"] ::text').get(),
                    'G': stats_season.css('td[data-stat="g"] ::text').get(),
                    'MP': stats_season.css('td[data-stat="mp"] ::text').get(),
                    'FG	': stats_season.css('td[data-stat="fg"] ::text').get(),
                    'FGA': stats_season.css('td[data-stat="fga"] ::text').get(),
                    'FG%': stats_season.css('td[data-stat="fg_pct"] ::text').get(),
                    '3P': stats_season.css('td[data-stat="fg3"] ::text').get(),
                    '3PA': stats_season.css('td[data-stat="fg3a"] ::text').get(),
                    '3P%': stats_season.css('td[data-stat="fg3_pct"] ::text').get(),
                    '2P': stats_season.css('td[data-stat="fg2"] ::text').get(),
                    '2PA': stats_season.css('td[data-stat="fg2a"] ::text').get(),
                    '2P%': stats_season.css('td[data-stat="fg2_pct"] ::text').get(),
                    'FT': stats_season.css('td[data-stat="ft"] ::text').get(),
                    'FTA': stats_season.css('td[data-stat="fta"] ::text').get(),
                    'FT%': stats_season.css('td[data-stat="ft_pct"] ::text').get(),
                    'ORB': stats_season.css('td[data-stat="orb"] ::text').get(),
                    'DRB': stats_season.css('td[data-stat="drb"] ::text').get(),
                    'TRB': stats_season.css('td[data-stat="trb"] ::text').get(),
                    'AST': stats_season.css('td[data-stat="ast"] ::text').get(),
                    'STL': stats_season.css('td[data-stat="stl"] ::text').get(),
                    'BLK': stats_season.css('td[data-stat="blk"] ::text').get(),
                    'TOV': stats_season.css('td[data-stat="tov"] ::text').get(),
                    'PF': stats_season.css('td[data-stat="pf"] ::text').get(),
                    'PTS': stats_season.css('td[data-stat="pts"] ::text').get()
                }