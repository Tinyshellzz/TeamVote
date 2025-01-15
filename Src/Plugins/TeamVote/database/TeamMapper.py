from .db_config import *
import datetime
import json

try:
    db = connect()
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS teams (
              name Varchar(48),
              president Char(36),
              vice_president Char(36),
              qq Char(12),
              home Varchar(128),
              color Char(7),
              abbr Char(16),
              UNIQUE KEY (name),
              KEY (president),
              KEY (vice_president),
              KEY (qq),
              KEY (abbr)
            ) ENGINE=InnoDB CHARACTER SET=utf8;""")
    db.commit()
    c.close()
    db.close()
except:
    pass

class Team:
    # permission 是权限等级，数字越高权限越大
    def __init__(self, name:str= None, president: str = None, vice_president: str = None, qq: str = None, home: str = None, color: str = None, abbr: str = None):
        self.name = name
        self.president = president
        self.vice_president = vice_president
        self.qq = qq
        self.home = home
        self.color = color
        self.abbr = abbr
    def __repr__(self) -> str:
        return json.dumps(self.__dict__, default=str)
    
class TeamMapper:
    def get_teams_by_representitive(qq: str):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT * FROM teams WHERE qq=%s", (qq,))
                res = c.fetchall()

        teams = []
        for r in res:
            teams.append(Team(r[0], r[1], r[2], r[3], r[4], r[5], r[6]))
        return teams
    
    def getTotalVoteCount():
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT COUNT(*) from teams INNER JOIN mc_players ON teams.name=mc_players.team WHERE teams.qq IS NOT NULL AND mc_players.owner IS NULL AND mc_players.active=1")
                res = c.fetchall()

        return res[0][0]
