# 负责处理简答的回复
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message
from pathlib import Path
from ..config.config import *
from ..utils import tools
import requests
import json
from random import randrange
from .authorization import *
from ..database.TeamMapper import TeamMapper

plugin_dir = str(Path(__file__).resolve().parents[1])

vote_started = False      # 投票是否开始
vote_count = []         # 组织:票数 的字典
for i in range(100):
    vote_count.append({})

# 入口函数
class test:
    async def handle(bot: Bot, event: Event):
        # 判断是否是群组事件, 不是就返回
        if not isinstance(event, GroupMessageEvent): return
        if not await auth(bot, event): return

        user_id = str(event.user_id)
        group_id = str(event.group_id)
        self_id = str(event.self_id)

        msg = (f"【服务器信息-地址】\n" +
               "-----------\n" +
               "首选IP:Tcc-mc.com\n" +
               "备用IP:Mc.tcc-mc.com\n" +
               "爱坤专用IP:i-kun.love\n" +
               "-----------\n" +
               "进不去的可以看群公告更改dns\n" +
               "-----------\n" +
               "更多请查阅【TCC玩家手册】\n" +
               "https://docs.qq.com/aio/DZGZrVFVqTERCTmNn&#34")

        messages = []
        messages.append(tools.to_msg_node(msg))
        await tools.send_forward_msg(bot, event, messages)

class vote_start:
    async def handle(bot: Bot, event: Event):
        # 判断是否是群组事件, 不是就返回
        if not isinstance(event, GroupMessageEvent): return
        if not await auth(bot, event): return

        global vote_started
        vote_started = True

        await bot.send(event, Message("请各组织代表开始投票，'1'表示同意, '2'表示反对, '3'表示弃权"))

class vote_end:
    async def handle(bot: Bot, event: Event):
        # 判断是否是群组事件, 不是就返回
        if not isinstance(event, GroupMessageEvent): return
        if not await auth(bot, event): return

        vote_outcome = ""
        vote_count_1 = []
        for i in range(100):
            counts = vote_count[i]
            vote_count_1.append(0)
            if len(counts) == 0: continue   # 该位置没有人投票

            if i == 1: 
                vote_outcome += f"{i}/同意: \n"
            elif i == 2: 
                vote_outcome += f"{i}/反对: \n"
            elif i == 3: 
                vote_outcome += f"{i}/弃权: \n"
            else:
                vote_outcome += f"{i}: \n"

            flag = False
            for team, count in counts.items():
                vote_outcome += f"{team}: {count}, "
                vote_count_1[i] += count
                flag = True
            if flag:
                vote_outcome = vote_outcome[:-2]    # 除去多余的 ", "
                vote_outcome += "\n"

        vote_outcome_final = ""
        voted_counts = 0
        for i in range(100):
            counts = vote_count_1[i]
            if counts == 0: continue
            if i == 1: 
                vote_outcome_final += f"\n{i}/同意: {counts}"
            elif i == 2: 
                vote_outcome_final += f"\n{i}/反对: {counts}"
            elif i == 3: 
                vote_outcome_final += f"\n{i}/弃权: {counts}"
            else:
                vote_outcome_final += f"\n{i}: {counts}"
            
            voted_counts += counts
        if(vote_outcome_final != ""):
            vote_outcome_final = vote_outcome_final[1:]  # 去除开头多余的"\n"

        total_vote_count = TeamMapper.getTotalVoteCount()

        # 清空标志位以及存储数组
        global vote_started
        vote_started = False
        for i in range(100):
            vote_count[i] = {}

        # 总票数是指，所有有代表的团队的票数之和，也就是所有能投票的活跃玩家数量
        # 投票参与是指，该次投票参与投票的人数
        await bot.send(event, Message(f'总票数: {total_vote_count}, 投票参与: {voted_counts}, 投票结果: \n{vote_outcome_final}'))
        messages = []
        messages.append(tools.to_msg_node(f'详细投票结果: \n{vote_outcome}'))
        await tools.send_forward_msg(bot, event, messages)
