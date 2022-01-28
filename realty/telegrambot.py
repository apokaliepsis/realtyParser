import asyncio
import urllib


import drop as drop
import requests
from aiogram import Bot, types



class TelegramBot:

    token = '5099072370:AAG4kydCgXarsDdHvxwf6Lum57MtQ-u2CSY'
    channel_id = -1001769787001  # это должен быть int, например -1006666666666
    bot = Bot(token=token, parse_mode=types.ParseMode.HTML)

    async def send_message(channel_id: int, url, text: str ):

        #await TelegramBot.bot.send_message(channel_id, text,f)
        await TelegramBot.bot.send_photo(channel_id, url,caption=text)

    def send_telegram(text: str):
        #token = "ТУТ_ВАШ_ТОКЕН_КОТОРЫЙ_ВЫДАЛ_BotFather"
        url = "https://api.telegram.org/bot"
        #channel_id = "@ИМЯ_КАНАЛА"
        url += TelegramBot.token
        method = url + "/sendMessage"

        r = requests.post(method, data={
            "chat_id": TelegramBot.channel_id,
            "text": text
        })

        if r.status_code != 200:
            raise Exception("post_text error")

if __name__ == '__main__':
    TelegramBot.send_telegram("hello world!")