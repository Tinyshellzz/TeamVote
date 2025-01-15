import logging
from pathlib import Path
import yaml
from shutil import copyfile

# create logger with 'TeamVoteBot'
logger = logging.getLogger('TeamVoteBot')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
plugin_dir = str(Path(__file__).resolve().parents[1])
print(plugin_dir)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler(plugin_dir + '/test.log', encoding='utf-8', mode="a")     # 最好每天生成一个新的 log
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

db_host="127.0.0.1"
db_port=3306
db_user="team"
db_passwd="NeoTccServer2025@"
db_database="team"
auth_group_list = ["536038559", "333"]       # bot工作qq群, 这些群里的人必须都是服务器玩家
auth_qq_list = ["3478848836", "333"]             # 部分命令允许的 qq号 (例如 /whitelist update)