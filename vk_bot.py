import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import Env

from dialog_flow_lib import fetch_intent_response


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )

def greeting(event, vk_api):
    user_id = event.user_id,
    message = event.text,

    response = fetch_intent_response(user_id, *message)
    vk_api.messages.send(
        user_id=user_id,
        message=response,
        random_id=random.randint(1,1000)
    )


def main():
    env = Env()
    vk_session = vk.VkApi(token=env.str('VK_API_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            greeting(event, vk_api)


if __name__ == '__main__':
    main()