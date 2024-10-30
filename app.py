from flask import Flask, request, send_from_directory

# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 引入 os 模組
import os

# 載入 LINE Message API 相關函式庫
# from linebot import LineBotApi
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import MessagingApi, Configuration
from linebot.v3.messaging.models import TextMessage, FlexMessage  # 確保導入正確的訊息類
# 引入 Weather API 天氣查詢
import weatherAPI

# 引入 traceback
import traceback

# 引入 dotenv
from dotenv import load_dotenv, dotenv_values


app = Flask(__name__)

access_token = dotenv_values('.env')["linebot_access_token"]
secret = dotenv_values('.env')["linebot_secret"]


@app.route("/", methods=['GET'])
def init():
    return ('Hello')


@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        # print('\n', json_data, '\n')

        # # 使用 Configuration 來設置 access_token
        configuration = Configuration(access_token=access_token)
        messaging_api = MessagingApi(configuration=configuration)  # 確認 token 是否正確
        handler = WebhookHandler(secret)

        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊

        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        userId = json_data['events'][0]['source']['userId']  # 取得使用者 ID
        msg_type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型
        if msg_type == 'text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息
            user_history(userId, 'user', msg)                # 紀錄user訊息

            if '天氣' in msg:
                reply = weatherAPI.get_weather(msg)     # 呼叫 get_weather_city 函式
                if reply is not None:
                    reply_json = FlexMessage(alt_text='天氣', contents=reply)
                    reply = '天氣資訊'
                    line_bot_api.reply_message(tk, reply_json)  # 回傳訊息
                    return 'OK'
                    messaging_api .reply_message(tk, reply_json)  # 回傳訊息
                    return 'OK'
                else:
                    reply = '無法查詢\n請重新輸入 "天氣" + "地區"'
            else:
                reply = msg  # 不是詢問天氣就重複使用者輸入內容
        else:
            reply = '你傳的不是文字呦～'

        user_history(userId, 'assistant', reply)
        # print('\n', reply, '\n')
        line_bot_api.reply_message(tk, TextSendMessage(reply))  # 回傳訊息
        # print('\n', reply, '\n')
        messaging_api .reply_message(tk, TextMessage(reply))  # 回傳訊息

    except Exception as e:                                      # 如果發生錯誤，印出收到的內容
        print("錯誤類型:", type(e).__name__)
        print("錯誤訊息:", e)
        print("錯誤行數:")
        traceback.print_exc()
    return 'OK'                                              # 驗證 Webhook 使用，不能省略


@app.route('/broadcast', methods=['POST'])
def boardcast():
    # # 使用 Configuration 來設置 access_token
    configuration = Configuration(access_token=access_token)
    messaging_api = MessagingApi(configuration=configuration)  # 確認 token 是否正確
    # handler = WebhookHandler(secret)

    body = request.get_data(as_text=True)
    try:
        json_data = json.loads(body)

        user = json_data.get("user")  # 取得使用者名稱（此處未使用）
        contents = json_data.get("content")

        for content in contents:
            msg_type = content["type"]
            msg = content["message"]

            if msg_type == "text":
                messaging_api.broadcast(TextMessage(text=msg))
            elif msg_type == "flex":
                messaging_api.broadcast(FlexMessage(alt_text="廣播", contents=msg))
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


def user_history(user_id, caracters, text):
    log_msg = {caracters: text}
    file_path = os.path.join('history_msg', f'{user_id}.json')

    try:
        if os.path.isfile(file_path):
            # 如果檔案已存在，讀取當前內容並添加新的訊息
            with open(file_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            # 如果檔案不存在，初始化為空陣列
            history = []

        # 添加新的訊息到歷史紀錄
        history.append(log_msg)

        # 將更新後的歷史紀錄寫回檔案
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f'寫入檔案時發生錯誤: {e}')


if __name__ == "__main__":

    app.run(debug=True)
