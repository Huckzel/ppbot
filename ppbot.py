"""
Telegram prettyprintbot

Huck Nuchelmans

file: ppbot.py
A simple Telegram bot that gives users the ability to use markdown.
"""

import urllib
import cStringIO
from PIL import Image
from telegram import Updater, InlineQueryResultArticle, InlineQueryResultPhoto
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('ppbot.conf')

UPDATER = Updater(token=parser.get('updater', 'token'))


def inline_pretty(bot, update):
    """ Pretty print a query. This can be markdown or LaTeX math. """
    if update.inline_query is not None:
        query = update.inline_query.query

        if query[0] == '$' and query[-1] == '$':
            # If the query is between dollar signs, interpret it as math.
            math_url = \
                r'https://latex.codecogs.com/png.latex?%5Cdpi%7B300%7D' + \
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

    dispatcher.addTelegramInlineHandler(inline_pretty)

    UPDATER.start_polling()


def stop():
    """ Stop the updater before exiting. """
    UPDATER.stop()


if __name__ == '__main__':
    start()
