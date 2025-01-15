from .db_config import *
import datetime
import json

try:
    db = connect()
    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS mc_players (
              name Varchar(48),
              uuid Char(36),
              team Varchar(48),
              login_time Varchar(256),
              owner Char(36),
              active Bool,
              KEY (name),
              UNIQUE KEY (uuid),
              KEY (team),
              KEY (login_time),
              KEY (owner),
              KEY (active)
            ) ENGINE=InnoDB CHARACTER SET=utf8;""")
    db.commit()
    c.close()
    db.close()
except:
    pass

class MCPlayer:
    # permission 是权限等级，数字越高权限越大
    def __init__(self, name:str= None, uuid: str = None, team: str = None, login_time: datetime.datetime = None, owner: str = None, active: bool = None):
        self.id = id
        self.name = name
        self.uuid = uuid
        self.team = team
        self.login_time = login_time
        self.owner = owner
        self.active = active
    def __repr__(self) -> str:
        return json.dumps(self.__dict__, default=str)
    
class MCPlayerMapper:
    def get_active_player_count_by_team(team_name: str):
        res = None
        with connect() as db:
            with db.cursor() as c:
                db.commit()
                c.execute("SELECT COUNT(*) from mc_players WHERE team=%s AND active=1 AND owner IS NULL", (team_name,))
                res = c.fetchall()

        return res[0][0]

