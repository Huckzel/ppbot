"""
Telegram prettyprintbot

Huck Nuchelmans

file: ppbot.py
A simple Telegram bot that gives users the ability to use markdown.
"""

import os
import urllib
import requests
import cStringIO
from PIL import Image
from telegram import Updater, InlineQueryResultArticle, InlineQueryResultPhoto

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
    math_url = math_url = \
        r'https://latex.codecogs.com/png.latex?%5Cdpi%7B600%7D' + \
        urllib.quote(expression)

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


def inline_pretty(bot, update):
    """ Pretty print a query. This can be markdown or LaTeX math. """
    if update.inline_query is not None:
        query = update.inline_query.query

        if query[0] == '$' and query[-1] == '$':
            # If the query is between dollar signs, interpret it as math.
            math_url = \
                r'https://latex.codecogs.com/png.latex?%5Cdpi%7B600%7D' + \
                urllib.quote(query[1:-1])

            # Get the dimensions of the image.
            tmp_file = cStringIO.StringIO(urllib.urlopen(math_url).read())
            width, height = Image.open(tmp_file).size

            results = [
                InlineQueryResultPhoto(
                    'MATH', math_url, math_url, mime_type='image/png',
                    photo_width=width, photo_height=height
                )
            ]
        else:
            results = [
                InlineQueryResultArticle(
                    'MD', 'Markdown', query, parse_mode='Markdown'
                ),
            ]

        bot.answerInlineQuery(update.inline_query.id, results)


def start():
    """ Handle telegram updates. """
    dispatcher = UPDATER.dispatcher

    dispatcher.addTelegramCommandHandler('math', math)
    dispatcher.addTelegramMessageHandler(markdown)
    dispatcher.addTelegramInlineHandler(inline_pretty)

    UPDATER.start_polling()


def stop():
    """ Stop the updater before exiting. """
    UPDATER.stop()


if __name__ == '__main__':
    start()
