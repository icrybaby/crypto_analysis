import requests

import Constants


class TelegramBot:
    def push_message(text):
        url = "https://api.telegram.org/bot" + Constants.TELEGRAM_BOT_TOKEN + "/sendMessage?chat_id=" + Constants.TELEGRAM_BOT_CHAT_ID + "&parse_mode=Markdown&text=" + text
        response = requests.get(url)
        print("Push message response: ", response.status_code)

        return True if response.status_code == Constants.SUCCESS_RESPONSE_CODE else False

