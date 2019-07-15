from flask import Flask, request, abort
import os

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)

app = Flask(__name__)

# 使用heroku的environment variables
line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回應使用者輸入的話
    
    message = ImageSendMessage(
        original_content_url = 'https://www.facebook.com/photo.php?fbid=975507332546305&set=a.102012123229168&type=3&theater',
        preview_image_url = 'https://www.facebook.com/photo.php?fbid=2192822987481394&set=a.102012123229168&type=3&theater'   
    )
    line_bot_api.reply_message(event.reply_token, message)
    '''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    '''

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    # Setting host='0.0.0.0' will make Flask available from the network
    app.run(host='0.0.0.0', port=port)
