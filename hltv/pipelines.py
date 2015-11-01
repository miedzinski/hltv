from dateutil.parser import parse as parse_date

from hltv.models import DBSession, Match, Map, Team


class MorphIOPipeline(object):
    def process_item(self, item, spider):
        session = DBSession()

        date = parse_date(item['date']).date()

        maps = [Map(name=map[0], score=map[1]) for map in item['maps']]

        score = self.calc_score(item['maps'])

        team1_name = item['teams'][0]
        team1_lineup = item['lineup1']

        team1 = Team.find_or_new(team1_name, team1_lineup)

        team2_name = item['teams'][1]
        team2_lineup = item['lineup2']

        team2 = Team.find_or_new(team2_name, team2_lineup)

        match = Match(hltv_id=item['id'],
                      date=date,
                      tournament=item['tournament'],
                      best_of=item['best_of'],
                      maps=maps,
                      score=score,
                      team1=team1,
                      team2=team2)

        session.add(match)
        session.commit()

        return item

    @staticmethod
    def calc_score(maps):
        team1_score = 0
        team2_score = 0
        for map in maps:
            try:
                score = map[1].split(':')[:2]
                score[1] = score[1].split()[0]
            except:
                break

            if score[0] > score[1]:
                team1_score += 1
            else:
                team2_score += 1

        return ':'.join([str(team1_score), str(team2_score)])
