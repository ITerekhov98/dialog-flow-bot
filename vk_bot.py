import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from environs import Env


def main():
    env = Env()
    vk_session = vk_api.VkApi(token=env.str('VK_API_TOKEN'))
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)

if __name__ == '__main__':
    main()