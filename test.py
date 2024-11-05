
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
if __name__ == '__main__':
    TextSendMessage('123')

    print(type(TextSendMessage('123')))
