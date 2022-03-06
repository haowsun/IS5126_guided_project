import scrapy
import re

class NBATeamSSSpider(scrapy.Spider):
    name = "nba_team_player"
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
                Team = stats_season.css('td[data-stat="team_name"] ::text').get()
                next_link = stats_season.css('th[data-stat="season"]').css('a ::attr(href)').get()
                if next_link is not None:
                    yield response.follow(next_link, meta={'Team': Team, 'Season': season}, callback=self.parse_team_player_page)

    def parse_team_player_page(self, response):
        team_players = response.css('div#div_roster tbody tr')
        for team_player in team_players:
            yield {
                'Team': response.meta['Team'],
                'Season': response.meta['Season'],
                'No.': team_player.css('th[data-stat="number"] ::text').get(),
                'Player': team_player.css('td[data-stat="player"] ::text').get(),
                'Pos': team_player.css('td[data-stat="pos"] ::text').get(),
                'Ht': team_player.css('td[data-stat="height"] ::text').get(),
                'Wt': team_player.css('td[data-stat="weight"] ::text').get(),
                'Birth Date': team_player.css('td[data-stat="birth_date"] ::text').get(),
                'Exp': team_player.css('td[data-stat="years_experience"] ::text').get(),
                'College': team_player.css('td[data-stat="college"] ::text').get(),

            }
