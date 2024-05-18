# internal_db_ops/feishu_api.py
import requests

class FeishuAPI:
    BASE_URL = "https://open.feishu.cn/open-apis"
    APP_ID = "your_app_id"  # 替换为你的 app_id
    APP_SECRET = "your_app_secret"  # 替换为你的 app_secret

    @staticmethod
    def get_access_token():
        url = f"{FeishuAPI.BASE_URL}/auth/v3/app_access_token/internal"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "app_id": FeishuAPI.APP_ID,
            "app_secret": FeishuAPI.APP_SECRET
        }
        response = requests.post(url, json=payload)
        response_data = response.json()
        return response_data.get("app_access_token")

    @staticmethod
    def get_user_id(contact):
        access_token = FeishuAPI.get_access_token()
        if not access_token:
            raise ValueError("Failed to get access token")

        url = f"{FeishuAPI.BASE_URL}/contact/v3/users/batch_get_id"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "mobiles": [contact] if "@" not in contact else [],
            "emails": [contact] if "@" in contact else []
        }
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response_data.get("code") == 0:
            user_list = response_data.get("data", {}).get("user_list", [])
            if user_list:
                return user_list[0].get("user_id")
        return None

    @staticmethod
    def get_user_info_by_id(user_id):
        access_token = FeishuAPI.get_access_token()
        if not access_token:
            raise ValueError("Failed to get access token")

        url = f"{FeishuAPI.BASE_URL}/contact/v3/users/{user_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response_data.get("code") == 0:
            user_data = response_data.get("data", {})
            user_info = {
                "name": user_data.get("name"),
                "mobile": user_data.get("mobile")
            }
            return user_info
        return None

    @staticmethod
    def create_group(name, user_ids):
        access_token = FeishuAPI.get_access_token()
        if not access_token:
            raise ValueError("Failed to get access token")

        url = f"{FeishuAPI.BASE_URL}/im/v1/chats"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "name": name,
            "user_id_list": user_ids
        }
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response_data.get("code") == 0:
            return response_data.get("data", {}).get("chat_id")
        else:
            raise ValueError(f"Failed to create group: {response_data.get('msg')}")

    @staticmethod
    def send_message(chat_id, message):
        access_token = FeishuAPI.get_access_token()
        if not access_token:
            raise ValueError("Failed to get access token")

        url = f"{FeishuAPI.BASE_URL}/im/v1/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "receive_id": chat_id,
            "content": {
                "text": message
            },
            "msg_type": "text",
            "receive_id_type": "chat_id"
        }
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        if response_data.get("code") == 0:
            return response_data.get("data", {}).get("message_id")
        else:
            raise ValueError(f"Failed to send message: {response_data.get('msg')}")

    def get_headers():
        access_token = FeishuAPI.get_access_token()
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }


    def send_message_to_chat(chat_id, card_json):
        url = f"{FeishuAPI.BASE_URL}/message/v4/send/"
        payload = {
            "chat_id": chat_id,
            "msg_type": "interactive",
            "card": card_json
        }
        response = requests.post(url, json=payload, headers=FeishuAPI.get_headers())
        response_data = response.json()
        if response.status_code != 200:
            raise ValueError(f"Failed to send message: {response_data.get('msg')}")
        return response_data.get('data', {}).get('message_id')

    def pin_message(chat_id, message_id):
        url = f"{FeishuAPI.BASE_URL}/chat/v4/pin"
        payload = {
            "chat_id": chat_id,
            "message_id": message_id
        }
        response = requests.post(url, json=payload, headers=FeishuAPI.get_headers())
        response_data = response.json()
        if response.status_code != 200:
            raise ValueError(f"Failed to pin message: {response_data.get('msg')}")
        return response_data

    def send_and_pin_message(chat_id, card_json):
        try:
            message_id = FeishuAPI.send_message_to_chat(chat_id, card_json)
            pin_response = FeishuAPI.pin_message(chat_id, message_id)
            return {"message_id": message_id, "pin_response": pin_response}
        except Exception as e:
            raise ValueError(f"Error in sending and pinning message: {str(e)}")

    def send_message_with_mention(chat_id, message, user_id):
        mention_format = f'<at user_id="{user_id}"></at>'
        full_message = f"{mention_format} {message}"
        payload = {
            "chat_id": chat_id,
            "msg_type": "text",
            "content": {
                "text": full_message
            }
        }
        url = f"{FeishuAPI.BASE_URL}/message/v4/send/"
        response = requests.post(url, json=payload, headers=FeishuAPI.get_headers())
        response_data = response.json()
        if response.status_code != 200:
            raise ValueError(f"Failed to send message: {response_data.get('msg')}")
        return response_data