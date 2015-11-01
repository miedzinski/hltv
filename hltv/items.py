from scrapy import Item, Field


class Match(Item):
    id = Field()
    date = Field()
    tournament = Field()
    best_of = Field()
    maps = Field()
    teams = Field()
    lineup1 = Field()
    lineup2 = Field()
