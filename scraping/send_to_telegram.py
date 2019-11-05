#!/usr/bin/env python3
# 
# this script sends piped in data to telegram chat using a telegram bot
#
# written by Hani Alshikh
#
####################################################################

import sys
import requests
import datetime
import config

def telegram_bot_sendtext(bot_message):

    """ send a given message to telegram chat """

    bot_token = config.telegram['bot_token']
    bot_chatID = config.telegram['bot_chatID']
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


# check for stdin input
if not sys.stdin.isatty():
  messeage = sys.stdin.read()

  if not messeage:
    print("%s: Nothing to send" % datetime.datetime.now())
    exit()

  if "-"*40 in messeage:
    for job in messeage.split("-"*40):
      send = telegram_bot_sendtext(str(job))
      print(send)

  else:
    send = telegram_bot_sendtext(str(messeage))
    print(send)
  exit()

# send a testing ping if there is nothing piped in
ping = telegram_bot_sendtext("ping")
print(ping)