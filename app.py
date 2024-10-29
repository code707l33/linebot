from flask import Flask, request

# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

# 引入 Weather API 天氣查詢
import weatherAPI

app = Flask(__name__)


with open('secret.json') as fp:
    secret_data = json.load(fp)

access_token = secret_data['access_token']
secret = secret_data['secret']


@app.route("/", methods=['GET'])
def init():
    return ('Hello')


@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        print('\n', json_data, '\n')
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers

        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token

        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type == 'text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息

            if '天氣' in msg:
                # reply = weatherAPI.get_weather(msg)     # 呼叫 get_weather_city 函式
                reply_json = FlexSendMessage(alt_text='天氣', contents={"type": "carousel", "contents": [{"type": "bubble", "size": "micro", "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "台北,內湖", "color": "#ffffff", "align": "start", "size": "20px", "gravity": "center"}, {"type": "text", "text": "10月29日6A.M.", "color": "#ffffff", "align": "start", "size": "xs", "gravity": "center", "margin": "lg"}], "backgroundColor": "#27ACB2",
                                             "paddingTop": "19px", "paddingAll": "12px", "paddingBottom": "16px"}, "body": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "陰天", "size": "18px"}, {"type": "text", "text": "降雨機率80%", "size": "15px"}, {"type": "box", "layout": "vertical", "contents": [], "backgroundColor": "#0D8186", "width": "80%", "height": "6px"}], "spacing": "md", "paddingAll": "12px"}, "styles": {"footer": {"separator": false}}}]})
                # line_bot_api.reply_message(tk, TextSendMessage(reply))  # 回傳訊息
                line_bot_api.reply_message(tk, reply_json)  # 回傳訊息
            else:
                line_bot_api.reply_message(tk, TextSendMessage(msg))  # 回傳訊息
        else:
            line_bot_api.reply_message(tk, TextSendMessage('你傳的不是文字呦～'))  # 回傳訊息

    except Exception as e:
        print(f'Error: {e}\n', body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                                              # 驗證 Webhook 使用，不能省略


if __name__ == "__main__":

    app.run()
