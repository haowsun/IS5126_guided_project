# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NBAPlayer(scrapy.Item):
    Name = scrapy.Field()
    Position = scrapy.Field()
    Height = scrapy.Field()
    Weight = scrapy.Field()
    Born = scrapy.Field()
    Recruiting_rank = scrapy.Field()
    Draft_team = scrapy.Field()
    Experience = scrapy.Field()
    Career_length = scrapy.Field()


class NBAPerformance(scrapy.Item):
    Name = scrapy.Field()
    Season = scrapy.Field()
    Age = scrapy.Field()
    Is_playoff = scrapy.Field()
    Tm = scrapy.Field()
    Lg = scrapy.Field()
    Pos = scrapy.Field()
    G = scrapy.Field()
    GS = scrapy.Field()
    MP = scrapy.Field()
    FG = scrapy.Field()
    FGA = scrapy.Field()
    FG_Percent = scrapy.Field()
    _3P = scrapy.Field()
    _3PA = scrapy.Field()
    _3P_Percent = scrapy.Field()
    _2P = scrapy.Field()
    _2PA = scrapy.Field()
    _2P_Percent = scrapy.Field()
    eFG_Percent = scrapy.Field()
    FT = scrapy.Field()
    FTA = scrapy.Field()
    FT_Percent = scrapy.Field()
    ORB = scrapy.Field()
    DRB = scrapy.Field()
    TRB = scrapy.Field()
    AST = scrapy.Field()
    STL = scrapy.Field()
    BLK = scrapy.Field()
    TOV = scrapy.Field()
    PF = scrapy.Field()
    PTS = scrapy.Field()


class NBASalary(scrapy.Item):
    Name = scrapy.Field()
    Season = scrapy.Field()
    Team = scrapy.Field()
    Lg = scrapy.Field()
    Salary = scrapy.Field()
