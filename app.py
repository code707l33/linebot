from flask import Flask, request, send_from_directory

# 載入 json 標準函式庫，處理回傳的資料格式
import json

# 引入 os traceback 模組
import os
from pathlib import Path
import traceback

# 引入 dotenv
from dotenv import load_dotenv, dotenv_values

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage

# 引入 Weather API 天氣查詢, GPT API 資料處理
import weatherAPI
import linebot_GPT


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
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers

        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token

        user_id = json_data['events'][0]['source']['userId']  # 取得使用者 ID
        msg_type = json_data['events'][0]['message']['type']     # 取得 LINe 收到的訊息類型

        if msg_type == 'text':
            msg = json_data['events'][0]['message']['text']  # 取得 LINE 收到的文字訊息

            # 判斷GPT HISTORY 是否存在，存在則調用GPT API 回復
            file_path = os.path.join('history_msg', f'{user_id}.json')
            file_path = Path(file_path)

            if msg.startswith(('!', '！')):              # 判斷是否為指令
                reply = command_handler(user_id, msg[1:], file_path)
            else:
                reply = message_handler(user_id, msg, file_path)
        else:
            reply = TextSendMessage('你傳的不是文字呦～')

        # user_history(userId, 'assistant', reply)
        # print('\n', reply, '\n')
        line_bot_api.reply_message(tk, reply)  # 回傳訊息

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


def user_history(user_id, role, content, content_type=''):
    log_msg = {'role': role, 'content': content, 'content_type': content_type}
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


def command_handler(user_id, msg, file_path):

    if msg.lower() == 'gpt':                             # 判斷是否為 GPT 指令
        if Path.exists(file_path):
            os.remove(file_path)
            return '-----關閉 GPT 模式-----'
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                init_gptMSG = [{"role": "system", "content": "你是一個聊天機器人，請用繁體中文回答"}]
                json.dump(init_gptMSG, f, ensure_ascii=False, indent=4)
            return '-----開啟 GPT 模式-----'

    elif '天氣' in msg:                             # 判斷是否為天氣指令
        reply = weatherAPI.get_weather(msg)
        if reply is not None:

            print('\n\n', type(FlexSendMessage(reply)), '\n\n')
            return FlexSendMessage(reply)
        else:
            print('\n\n', type(TextSendMessage('無法查詢\n請重新輸入 "!天氣" + "地區"')), '\n\n')
            return TextSendMessage('無法查詢\n請重新輸入 "!天氣" + "地區"')
    else:
        return TextSendMessage('!指令錯誤')


def message_handler(user_id, msg, file_path):

    if Path.exists(file_path):                        # 判斷是處於GPT 模式
        reply = linebot_GPT.chat_input(user_id, msg)
        user_history(user_id, 'user', msg)
        user_history(user_id, 'assistant', reply)
    else:
        reply = msg
    return TextSendMessage(reply)


if __name__ == "__main__":

    app.run(debug=True)
