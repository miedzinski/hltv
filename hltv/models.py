from sqlalchemy import (
    Column,
    Table,
    Integer,
    Date,
    String,
    ForeignKey,
)

from sqlalchemy import create_engine

from sqlalchemy.orm import scoped_session, sessionmaker

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///data.sqlite')
DBSession = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


class Match(Base):
    __tablename__ = 'data'

    hltv_id = Column(Integer, primary_key=True)
    date = Column(Date)
    tournament = Column(String)
    best_of = Column(Integer)
    score = Column(String)
    team1_id = Column(ForeignKey('team.id'))
    team2_id = Column(ForeignKey('team.id'))

    maps = relationship('Map')
    team1 = relationship('Team', primaryjoin='Match.team1_id == Team.id')
    team2 = relationship('Team', primaryjoin='Match.team2_id == Team.id')


class Map(Base):
    __tablename__ = 'map'

    id = Column(Integer, primary_key=True)
    match = Column(Integer, ForeignKey('data.hltv_id'))
    name = Column(String)
    score = Column(String)


lineup = Table('lineup',
               Base.metadata,
               Column('player_id', Integer, ForeignKey('player.id')),
               Column('team_id', Integer, ForeignKey('team.id')))


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    hltv_id = Column(Integer)
    nickname = Column(String)

    @classmethod
    def find_or_new(cls, hltv_id, nickname):
        session = DBSession()

        player = session.query(Player).filter_by(hltv_id=hltv_id).first()

        if not player:  # there is no such player in hltv db, maybe we have him?
            player = session.query(Player)\
                .filter((Player.nickname == nickname) & (Player.hltv_id is None)).first()

        if not player:  # there is no such player at all
            if not hltv_id:
                hltv_id = None
            player = Player(hltv_id=hltv_id, nickname=nickname)
            session.add(player)

        return player


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    players = relationship('Player', secondary=lineup, backref='teams')

    @classmethod
    def find_or_new(cls, name, players):
        session = DBSession()

        player_hltv_ids = [player[0] for player in players]

        # on first attempt we try to find teams by their lineups with player
        # from hltv database (they have hltv_ids)
        team = session.query(Team).join(Player.teams)\
            .filter((Team.name == name) & (Player.hltv_id.in_(player_hltv_ids))).first()

        if not team:
            # we don't have such team in our database
            # or we've got a player with no hltv_id
            # we'll create new team
            team = Team(name=name, players=[Player.find_or_new(p[0], p[1])
                                            for p in players])
            session.add(team)

        return team
