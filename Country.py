import sys
import os
import json
import re
import asyncio
import random
import telepot.aio
from telepot.namedtuple import  ReplyKeyboardMarkup, KeyboardButton, ForceReply, ReplyKeyboardRemove
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from time import strftime


async def on_chat_message(msg):
    global asnwerData, lowercaseCountries

    content_type, chat_type, chat_id = telepot.glance(msg)
    chat_id_str = str(chat_id)

    print(chat_id_str + " May be added to Chat id")

    with open('countrycap.log', 'a', encoding='utf8') as logFile:
        if content_type != 'text':
            return
        # logFile.write('[' + strftime("%Y-%m-%d %H:%m:%s")+'] [' + chat_id + '-> bot]: ' + msg['text'] + '\n')
        # print('Chat:', content_type, chat_type, chat_id)
        # print('User '+chat_id_str + ' wrote:\n' + msg['text'].lower())
        request = msg['text']

        if request in ('/start', 'hi', 'hello'):
            await bot.sendMessage(chat_id, answerData['Welcome'])
            # logFile.write('[' + strftime("%Y-%m-%d %H:%m:%s") + '] [' + chat_id_str + '-> bot]: ' + answerData['Welcome'] + '\n')
            return
        elif request in ('test'):

            testAnswers = ['Tashkent', 'Moscow', 'London', 'New York']
            inline_keyboard = []

            for a in range(len(testAnswers)):
                inline_keyboard.append([InlineKeyboardButton(text=testAnswers[a], callback_data=testAnswers[a])])
            ikm = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
            await bot.sendMessage(chat_id, "Choose below", reply_markup=ikm)

        elif request in asnwerData['countries'].keys():
            se = random.randint(0,1)
            phrase_Number = random.randint(0,4)
            if se==0:
                add = answerData['addsToAnswer']['start'][phrase_Number]
                await bot.sendMessage(chat_id, add + answerData['countries'][request])
                logFile.write('[' + strftime("%y-%m-%d %h:%m:%s") + '] [' + chat_id_str + ']' + add + answerData['countries'][request] + '\n')
            else:
                add = answerData['addsToAnswer']['end'][phrase_Number]
                await bot.sendMessage(chat_id, answerData['countries'][request] + '.' + add)
                logFile.write('[' + strftime("%y-%m-%d %h:%m:%s") + '] [' + chat_id_str + ']' + answerData['countries'][request] + add + '\n')
            return

        elif request in lowercaseCountries:
            await bot.sendMessage(chat_id, answerData['lowercaseCountryRequest'])
            logFile.write('[' + strftime("%y-%m-%d %h:%m:%s") + '] [' + chat_id_str + ']' + answerData['countries'] + '\n')

        else:
            await bot.sendMessage(chat_id, answerData['badRequest'])


async def on_callback_query(msg):
    global answerData
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(query_data)

    if query_data == answerData['countries']['Uzbekistan']:
        await bot.sendMessage(from_id, 'Correct!')
    else:
        await bot.sendMessage(from_id, 'It is not correct!')


homeDir = os.path.dirname(__file__)
lowercaseCountries = []
with open(os.path.join(homeDir, 'answersData.json'), encoding='utf8') as AnswersFile:
    print('Loading meta ...')
    answerData = json.load(AnswersFile)
    for country in answerData['countries'].keys():
        lowercaseCountries.append(country.lower())
    print('answer is loaded')


TOKEN = "377155013:AAEOws9pusC4F5X7Ibl5dSrgI-JQ6EnbppA"
bot = telepot.aio.Bot(TOKEN)

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query}))
print('Listening...')

loop.run_forever()