import re

from scrapy import Request
from scrapy.spiders import Spider

from hltv.items import Match


class ResultsSpider(Spider):
    name = "results"
    start_urls = ["http://www.hltv.org/results/"]

    def parse_result(self, response):
        match = Match()

        match['id'] = int(response.url.split('/')[-1].split('-')[0])

        match_div = response.selector.css(
            '#back > div.mainAreaNoHeadline > div.centerNoHeadline > div'
        )

        match['date'] = match_div.css('span')[3].xpath('text()')[0].extract()

        match['tournament'] = match_div.css(
            'div:nth-child(13) > div:nth-child(5)'
        ).xpath('a/text()')[0].extract()

        match['teams'] = tuple(match_div.css(
            'div:nth-child(13) > div:nth-child(1)'
        ).xpath('span/a/text()').extract())

        match['best_of'] = 0

        map_div = match_div.css(
            'div:nth-child(13) > div:nth-child(7) > div.hotmatchbox > div'
        )

        match['maps'] = []

        for i, _ in enumerate(map_div):
            try:
                map_img = map_div[i * 3 + 1].xpath('img/@src')[0].extract()
                map = map_img.split('/')[-1].split('.')[0]
                # strip html tags first, then remove repeating whitespace
                score = ' '.join(re.sub(r'<[^>]*>', '', map_div[i * 3 + 2].extract()).split())

                match['maps'].append((map, score))
                match['best_of'] += 1
            except:
                pass

        try:
            team1_lineup_div = match_div.css(
                'div:nth-child(13) > div:nth-child(22) > div'
            )

            match['lineup1'] = self.parse_lineups(team1_lineup_div)

            team2_lineup_div = match_div.css(
                'div:nth-child(13) > div:nth-child(26) > div'
            )

            match['lineup2'] = self.parse_lineups(team2_lineup_div)
        except IndexError:  # there is no div with scoreboard
            team1_lineup_div = match_div.css(
                'div:nth-child(13) > div:nth-child(16) > div'
            )

            match['lineup1'] = self.parse_lineups(team1_lineup_div)

            team2_lineup_div = match_div.css(
                'div:nth-child(13) > div:nth-child(20) > div'
            )

            match['lineup2'] = self.parse_lineups(team2_lineup_div)

        return match

    def parse_lineups(self, lineup_div):
        lineup = []

        for i in xrange(5):
            player_span = lineup_div[i * 2].css('div > span')
            player = self.parse_player(player_span)
            lineup.append(player)

        return lineup

    def parse_player(self, player_span):
        try:
            id = int(player_span.xpath('a/@href')[0].extract()\
                     .split('playerid=')[1].split('&')[0])
            nickname = player_span.xpath('a/span/text()')[0].extract()
        except IndexError:  # player has no hltv page => no hltv id
            id = None
            nickname = player_span.xpath('text()')[0].extract().strip()

        return id, nickname

    def parse(self, response):
        result_div = response.selector.css(
            '#back > div.mainAreaNoHeadline > div.centerNoHeadline > div'
        )

        for result in result_div.css('div.matchActionCell > a').xpath('@href'):
            url = 'http://www.hltv.org' + result.extract()
            yield Request(url, callback=self.parse_result)

        next = result_div.css('div.paginate > ul > a').xpath('@href')[1]
        url = 'http://www.hltv.org' + next.extract()

        yield Request(url)
