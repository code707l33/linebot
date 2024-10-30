from flask import Flask, request, send_from_directory

# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

# 引入 Weather API 天氣查詢
import weatherAPI

# 引入 traceback
import traceback

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
        # print('\n', json_data, '\n')
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers

        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token

        type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if type == 'text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息

            if '天氣' in msg:
                reply = weatherAPI.get_weather(msg)     # 呼叫 get_weather_city 函式

                if reply is None:
                    line_bot_api.reply_message(tk, TextSendMessage('無法查詢\n請重新輸入 "天氣" + "地區"'))
                else:
                    reply_json = FlexSendMessage(alt_text='天氣', contents=reply)
                    # line_bot_api.reply_message(tk, TextSendMessage(reply))  # 回傳訊息
                    line_bot_api.reply_message(tk, reply_json)  # 回傳訊息
            else:
                line_bot_api.reply_message(tk, TextSendMessage(msg))  # 回傳訊息
        else:
            line_bot_api.reply_message(tk, TextSendMessage('你傳的不是文字呦～'))  # 回傳訊息

    except Exception as e:                                      # 如果發生錯誤，印出收到的內容
        print("錯誤類型:", type(e).__name__)
        print("錯誤訊息:", e)
        print("錯誤行數:")
        traceback.print_exc()
    return 'OK'                                              # 驗證 Webhook 使用，不能省略


@app.route('/broadcast', methods=['POST'])
def boardcast():
    line_bot_api = LineBotApi(access_token)
    handler = WebhookHandler(secret)

    body = request.get_data(as_text=True)
    try:
        json_data = json.loads(body)

        user = json_data.get("user")  # 取得使用者名稱（此處未使用）
        contents = json_data.get("content")

        for content in contents:
            msg_type = content["type"]
            msg = content["message"]

            if msg_type == "text":
                line_bot_api.broadcast(TextSendMessage(text=msg))
            elif msg_type == "flex":
                line_bot_api.broadcast(FlexSendMessage(alt_text="廣播", contents=msg))
        return '200 Broadcast successful', 200  # 成功回應

    except Exception as e:
        print("錯誤類型:", type(e).__name__)
        print("錯誤訊息:", e)
        print("錯誤行數:")
        traceback.print_exc()
        return f'500 Error: {e}', 500  # 回應錯誤訊息和狀態碼


@app.route('/img/<filename>')
def serve_image(filename):
    # 指定圖片的文件夾路徑，並返回圖片文件
    return send_from_directory('static/images', filename)


if __name__ == "__main__":

    app.run(debug=True)
