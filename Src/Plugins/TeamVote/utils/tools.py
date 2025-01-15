import requests
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.adapters.onebot.v11 import Bot, Event
from ..config.config import *
from .MyException import MyException
from os import listdir
from os.path import isfile, join

num = 0

def get_uuid_by_name(user_name):
    url = f'https://api.mojang.com/users/profiles/minecraft/{user_name}?'
    response = requests.get(url)
    data = response.json()
    # 不是合法 user_name
    if 'errorMessage' in data: 
        return None
    
    mc_uuid = data['id']
    return mc_uuid

def get_name_and_uuid_by_name(user_name):
    url = f'https://api.mojang.com/users/profiles/minecraft/{user_name}?'
    response = requests.get(url)
    data = response.json()
    # 不是合法 user_name
    if 'errorMessage' in data: 
        return None
    
    mc_uuid = data['id']
    return (data['name'], mc_uuid)

def get_name_by_uuid(uuid):
    uuid = uuid.replace('-', '')
    url = f'https://api.mojang.com/user/profile/{uuid}'
    response = requests.get(url)
    data = response.json()

    # 不是合法 uuid
    if 'errorMessage' in data: 
        return None
    
    user_name = data['name']
    return user_name


async def send_forward_msg(bot: Bot, event: Event, messages):
    res_id = await bot.call_api("send_forward_msg", group_id=event.group_id, messages=messages)
    print(res_id)
    await bot.send(event, MessageSegment.forward(res_id))

def to_msg_node(msg):
    ret = {
                "type": "node",
                "data": {
                    "name": "TeamVoteBot",
                    "uin": "3975252362",
                    "content": [MessageSegment.text(msg)],
                },
        }
    
    return ret
    
def to_image_node(fpath):
    ret = {
                "type": "node",
                "data": {
                    "name": "TeamVoteBot",
                    "uin": "3975252362",
                    "content": [MessageSegment.image(fpath)],
                },
        }
    
    return ret

async def get_user_info(bot: Bot, event: Event, user_id):
    return await bot.call_api('get_stranger_info', user_id=user_id)

async def get_nick_name(bot: Bot, event: Event, user_id):
    info = await get_user_info(bot, event, user_id)
    return info.get('nickname')

def get_args(msg: str):
    l = len(msg)
    L = 0
    R = 0
    ret = []
    while True:
        while R < l and msg[R] != ' ': R += 1
        ret.append(msg[L:R])
        if R == l: break
        L = R

        while R < l and msg[R] == ' ': R+=1
        if R == l: break
        L = R
    
    return ret


def exception(msg):
    return MyException(msg)

def debug(msg):
    logger.debug(msg)

def info(msg):
    logger.info(msg)