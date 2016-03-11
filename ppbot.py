"""
Telegram prettyprintbot

Huck Nuchelmans

file: ppbot.py
A simple Telegram bot that gives users the ability to use markdown.
"""

import os
import requests
from telegram import Updater, InlineQueryResultArticle

UPDATER = Updater(token=os.environ['TOKEN'])


def markdown(bot, update):
    """ Echo a user's message, parsing any markdown. """
    bot.sendMessage(
        chat_id=update.message.chat_id,
        text=update.message.text,
        parse_mode='Markdown'
    )


def math(bot, update, args):
    """ Convert a text to a LaTeX Math image. """
    expression = ' '.join(args)
    math_url = r'http://latex.codecogs.com/png.latex?\dpi{300}%s' % expression

    file_name = 'img/%s.png' % hash(expression)
    tmp_file = open(file_name, 'wb')
    tmp_file.write(requests.get(math_url).content)
    tmp_file.close()

    tmp_file = open(file_name)
    bot.sendPhoto(
        chat_id=update.message.chat_id,
        photo=tmp_file
    )
    tmp_file.close()
    os.remove(file_name)


def inline_markdown(bot, update):
    """ Echo a user's inline query, parsing any markdown. """
    if update.inline_query is not None:
        query = update.inline_query.query

        results = [
            InlineQueryResultArticle(
                query, 'Markdown', query, parse_mode='Markdown',
                description=query
            )
        ]

        bot.answerInlineQuery(update.inline_query.id, results)


def start():
    """ Handle telegram updates. """
    dispatcher = UPDATER.dispatcher

    dispatcher.addTelegramCommandHandler('math', math)
    dispatcher.addTelegramMessageHandler(markdown)
    dispatcher.addTelegramInlineHandler(inline_markdown)

    UPDATER.start_polling()


def stop():
    """ Stop the updater before exiting. """
    UPDATER.stop()


if __name__ == '__main__':
    start()
