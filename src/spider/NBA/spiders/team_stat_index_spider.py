import scrapy
import re

class NBATeamSSSpider(scrapy.Spider):
    name = "nba_team_seasional_statistics"
    start_urls = ['https://www.basketball-reference.com/teams/']

    def parse(self, response):
        teams_table = response.css('table#teams_active tbody tr')
        for team in teams_table:
            team_page = team.css('th a::attr(href)').get()
            if team_page is not None:
                yield response.follow(team_page, callback=self.parse_team_page)
    def parse_team_page(self, response):
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
                    'Team': stats_season.css('td[data-stat="team_name"] ::text').get(),
                    'W': stats_season.css('td[data-stat="wins"] ::text').get(),
                    'L': stats_season.css('td[data-stat="losses"] ::text').get(),
                    'W/L%': stats_season.css('td[data-stat="win_loss_pct"] ::text').get(),
                    'Finish': stats_season.css('td[data-stat="rank_team"] ::text').get(),
                    'SRS': stats_season.css('td[data-stat="srs"] ::text').get(),
                    'Pace': stats_season.css('td[data-stat="pace"] ::text').get(),
                    'Rel Pace': stats_season.css('td[data-stat="pace_rel"] ::text').get(),
                    'ORtg': stats_season.css('td[data-stat="off_rtg"] ::text').get(),
                    'Rel ORtg': stats_season.css('td[data-stat="off_rtg_rel"] ::text').get(),
                    'DRtg': stats_season.css('td[data-stat="def_rtg"] ::text').get(),
                    'Rel DRtg': stats_season.css('td[data-stat="def_rtg_rel"] ::text').get(),
                    'Playoffs': stats_season.css('td[data-stat="rank_team_playoffs"] ::text').get(),
                    'Coaches': stats_season.css('td[data-stat="coaches"] ::text').get(),
                    'Top WS': stats_season.css('td[data-stat="top_ws"] ::text').get(),
                }