# coding: utf-8

import json
import os
import sys
import config
#import logging
#logging.getLogger().setLevel( logging.DEBUG )

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

import flask

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)

app = flask.Flask(__name__)

#CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi('ACCESS_TOKEN')
#CANNEL_SECRET
handler = WebhookHandler('CHANNEL_SECRET')

# Instantiates a client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'JSON_LINE_FILE'
client = language.LanguageServiceClient()

#返信メッセージを設定
msglst ={100:"全然問題ない!!!",
        90:"全然問題ない!!",
        80:"全然問題ない!",
        70:"問題ない!!!",
        60:"問題ない!!",
        50:"問題ない!",
        40:"大丈夫",
        30:"たぶん大丈夫",
        20:"まだ大丈夫",
        10:"もう少し大丈夫",
        0:"ギリギリ大丈夫",
        -10:"様子見しますか",
        -20:"もう少し様子見しますか",
        -30:"あと少し様子見しますか",
        -40:"少し機嫌が悪いかも。落ち着こう",
        -50:"機嫌が悪いかも。何かしたか思い出せ",
        -60:"ちょっとやばいかも。。",
        -70:"少しフォロー必要かも",
        -80:"フォロー必要",
        -90:"まずは謝ろう",
        -100:"土下座しよう"
    }

@app.route("/")
def hello():
    return "hello this page is nothing."


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = flask.request.headers['X-Line-Signature']

    # get request body as text
    body = flask.request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        flask.abort(400)

    return 'OK'

@handler.add(MessageEvent, message = TextMessage)
def handle_message(event):



    text = event.message.text

    document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    #score = round(sentiment.score, 1)
    score = int(sentiment.score * 100)
    ret = 'Sentiment: {}, {}'.format(sentiment.score,score)

    textresponse = str(score) + "点\n" + msglst[round(score,-1)]

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=textresponse))


if __name__ == "__main__":
    app.run()