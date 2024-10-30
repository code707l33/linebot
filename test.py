import requests
import json
from dotenv import load_dotenv, dotenv_values

# 設定請求 URL
url = "https://https.extension.phind.com/agent/"

# 設定請求頭
headers = {
    "Content-Type": "application/json",
    "User-Agent": "",  # 可留空或填入所需的 User-Agent
    "Accept": "*/*",
    "Accept-Encoding": "Identity"
}


def phind(text):
    # 設定請求資料
    data = {
        "additional_extension_context": "",
        "allow_magic_buttons": True,
        "is_vscode_extension": True,
        "message_history": [
            {
                "content": "",
                "role": "user"
            }
        ],
        "requested_model": "Phind-70B",
        "user_input": "你可以簡單的介紹你自己嗎？"
    }

    # 發送 POST 請求
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # 輸出回應
    if response.status_code == 200:
        # 拆分回應內容，提取有效的 JSON 資料
        response_text = response.text
        json_data = []

        # 逐行處理每一行，提取 JSON 部分
        for line in response_text.splitlines():
            if line.startswith("data: "):
                json_str = line[len("data: "):]  # 去除 "data: " 前綴
                try:
                    json_data.append(json.loads(json_str))
                except json.JSONDecodeError:
                    print("無法解析的 JSON:", json_str)

        # 輸出解析後的 JSON 資料
        msg = ''
        for item in json_data[1:]:

            finished = item['choices'][0]['finish_reason']
            if finished is None:
                try:
                    msg += item['choices'][0]['delta']['content']
                except Exception as e:
                    print(item)
                    break
            else:
                msg += '\n'
        print(msg)
    else:
        print("Error:", response.status_code)
        print("Response text:", response.text)  # 打印回應內容


if __name__ == '__main__':
    print()
