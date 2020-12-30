from __future__ import unicode_literals
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from datetime import datetime
import youtube_dl
import re
import os
import logging
import time
import json
# Enable logging

'''
logging.basicConfig(filename='Logs/{:%Y-%m-%d}.log'.format(datetime.now()),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.ERROR)
'''

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.ERROR)
					 
logger = logging.getLogger(__name__)

LINK_REGEX = r"(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"

requests = []

with open('/root/conf/config.json') as f:
    config = json.load(f)

telegram_token = config['telegram_token']
user_chat_id = config['user_chat_id']
downloads_path = '/downloads/'


def start(update, context):
    update.message.reply_text(
        "此机器人是视频下载机器人,测试阶段,不保证稳定!\n\n" +
        "可用命令:\n\n" +
		"/start		开始\n" +
		"/mp4		下载视频\n" +
		"/mp3		下载音频\n")

def mp4(update, context):
    if update.message.chat_id not in user_chat_id:
        update.message.reply_text(
            '您无权执行此操作！')
        return
    link = link_search(update.message.text)
    date = '{:%Y-%m-%d}'.format(datetime.now())
    if link:
        ydl_opts = {
#            'format': 'mp4',
            'quiet': True,
            'outtmpl': downloads_path + date + '_%(id)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            video_id = info_dict.get("id", None)
            video_ext = info_dict.get("ext", None)
            ydl.download([link])
        video = date + '_{0}.{1}'.format(video_id, video_ext)
        os.utime(downloads_path + video, (time.time(), time.time()))
        video_size = os.path.getsize(downloads_path + video)
        if video_size < 50000000:
            context.bot.send_video(chat_id=update.message.chat_id, video=open(
                downloads_path + video, 'rb'), timeout=1000)
            update.message.reply_text(
                '视频:' + video +' 下载成功！')
        else:
            update.message.reply_text(
                '视频:' + video +' 下载成功！')
    else:
        update.message.reply_text('该URL无效！')

def mp3(update, context):
    if update.message.chat_id not in user_chat_id:
        update.message.reply_text(
            '您无权执行此操作！')
        return
    link = link_search(update.message.text)
    date = '{:%Y-%m-%d}'.format(datetime.now())
    if link:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'outtmpl': downloads_path + date + '_%(id)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_id = info_dict.get("id", None)
            audio_ext = 'mp3'
            ydl.download([link])
        audio = date + '_{0}.{1}'.format(audio_id, audio_ext)
        os.utime(downloads_path + audio, (time.time(), time.time()))
        audio_size = os.path.getsize(downloads_path + audio)
        if audio_size < 50000000:
            context.bot.send_audio(chat_id=update.message.chat_id, audio=open(
                downloads_path + audio, 'rb'), timeout=1000)
            update.message.reply_text(
                '音频:' + audio +' 下载成功！')    
        else:
            update.message.reply_text(
                '音频:' + audio +' 下载成功！')
    else:
        update.message.reply_text('该URL无效')


def link_search(message):
    link = re.search(LINK_REGEX, message)
    if link:
        return link.group(0)
    else:
        return ""

def error(update, context):
    update.message.reply_text('下载失败\n发生错误!')
    logger.error('更新 "%s" 引起的错误 "%s"\n', update, context.error)

def main():
    updater = Updater(telegram_token, use_context=True, request_kwargs={
                      'read_timeout': 1000, 'connect_timeout': 1000})
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('mp4', mp4))
    dp.add_handler(CommandHandler('mp3', mp3))
    dp.add_handler(MessageHandler(Filters.text, mp4))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()