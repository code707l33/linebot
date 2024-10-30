from openai import OpenAI
import json
import os

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="sk-4EUIxGbV1foWL8XFpSYt74o61JnFivv6xx3W7MtxEGWMqAYl",
    # base_url="https://api.chatanywhere.tech/v1"
    base_url="https://api.chatanywhere.org/v1"
)


def chat_input(user_id, new_text):

    file_path = os.path.join('history_msg', f'{user_id}.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        history = json.load(f)

    messages = [
        {key: value for key, value in entry.items() if key != 'content_type'}
        for entry in history if entry['content_type'] == 'GPT']

    if len(messages) == 0:  # 如果沒有任何消息
        messages = [{"role": "system", "content": "你是一個聊天機器人，使用繁體中文回應"}]

    # 將用戶的輸入轉成字典格式
    user_msg = {"role": "user", "content": new_text}
    messages.append(user_msg)

    # 如果消息數量超過某個值，則刪除最舊的消息
    if len(messages) > 20:  # 例如，最多保留最近的 20 條消息
        messages.pop(0)  # 刪除最舊的消息

    # 呼叫 OpenAI API 並取得回覆
    completion = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        # model="embedding",
        model="gpt-4o-mini",
        # model="gpt-4",
        messages=messages
    )
    # 取得 GPT-3.5 的回覆
    gpt_msg = completion.choices[0].message.content
    # gpt_msg = "你好"
    messages.append({"role": "assistant", "content": gpt_msg})

    # 如果消息數量超過某個值，則刪除最舊的消息
    while len(messages) > 20:  # 例如，最多保留最近的 20 條消息
        messages.pop(0)  # 刪除最舊的消息

    return gpt_msg  # 只返回最新助手的回覆內容


if __name__ == "__main__":
    user_id = 'test'
    new_text = '你好'
    prompt = chat_input(user_id, new_text)
    print(prompt)
