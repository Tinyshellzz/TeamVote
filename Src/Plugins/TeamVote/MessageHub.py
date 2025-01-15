# 集中处理各种消息事件
from nonebot import on_message
from nonebot.adapters.onebot.v11.message import Message
from nonebot.adapters.onebot.v11 import Bot, Event
from .core import replies
from datetime import datetime
from .config.config import *
from .database.MCPlayerMapper import MCPlayerMapper
from .database.TeamMapper import TeamMapper
import re
matcher=on_message()
cooldown_dicts = []


# [正则, 方法, 冷却(s)]  (会默认调用status.py里面的 handle(bot, event) 方法)
match_rules = [
    ['^test$', replies.test, 0],
    ['^投票开始$', replies.vote_start, 0],
    ['^投票结束$', replies.vote_end, 0],
]


@matcher.handle()
async def _(bot: Bot, event: Event):
    # await bot.send(event, Message("received message: " + str(event.get_message())))

    for i in range(len(match_rules)):
        cooldown_dicts.append({})

    log = event.get_log_string()
    msg = re.search('\'(.+)\'', log)
    msg = msg.groups()[0]
    # print(msg)
    for i in range(len(match_rules)):
        rule = match_rules[i]
        if re.search(rule[0], msg) != None:
            if await cooldown(bot, event, rule[2], i):
                await rule[1].handle(bot, event)
            break
    
    user_id = str(event.user_id)
    if replies.vote_started == True:
        match = re.search('^([0-9]{1,2}|同意|反对|弃权)$', msg)
        if match == None: return    # 1-2位数字，或同意|反对|弃权 是合法投票消息
        match = match.groups()[0].strip()
        if match == "同意": match = 1
        elif match == "反对": match = 2
        elif match == "弃权": match = 3
        match = int(match)
    
        teams = TeamMapper.get_teams_by_representitive(user_id)
        if len(teams) == 0: return   # 该QQ不是代表


        msg = ""
        for team in teams:
            count = MCPlayerMapper.get_active_player_count_by_team(team.name)
            replies.vote_count[match][team] = count
            msg += f"{team}, "
        if msg != "":
            msg = msg[:-2]
        
        await bot.send(event, Message(f"[CQ:at,qq={user_id}] {msg} 投票成功"))
        


# 各个命令的冷却时间
async def cooldown(bot: Bot, event: Event, cooldown_time, i):
    cooldown_dict = cooldown_dicts[i]

    current_time = datetime.now()
    user_id = str(event.user_id)
    # 判断用户在不在冷却时间
    if user_id in cooldown_dict:
        last_call = cooldown_dict[user_id]
        time_diff = (current_time - last_call).total_seconds()
        if time_diff < cooldown_time:
            last_time_diff = int(cooldown_time - int(time_diff))
            await bot.send(event, Message(f"[CQ:at,qq={user_id}] 诶,我也是需要休息的,请{last_time_diff}秒后再试吧😘"))
            return False
    cooldown_dict[user_id] = current_time
    return True
