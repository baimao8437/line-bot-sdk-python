from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    BroadcastRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

import os

app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None))

# domain root
@app.route('/')
def home():
    print(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
    return 'Hello, World!'

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        res = line_bot_api.broadcast(BroadcastRequest(messages=[TextMessage(text=body)]))
        print("The response of MessagingApi->broadcast:\n")

    return 'OK'


if __name__ == "__main__":
    app.run()
