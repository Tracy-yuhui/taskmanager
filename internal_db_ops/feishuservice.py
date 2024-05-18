# internal_db_ops/feishu_service.py
from .feishu_api import FeishuAPI
from tasks.models import FeishuUser
from tasks.constants import generate_reminder_card
import threading


participants_list = []

class FeishuService:

    @staticmethod
    def store_user_info(contact):
        user_id = FeishuAPI.get_user_id(contact)
        if not user_id:
            raise ValueError("User not found")

        user_info = FeishuAPI.get_user_info_by_id(user_id)
        if not user_info:
            raise ValueError("Error fetching user info")

        feishu_user, created = FeishuUser.objects.update_or_create(
            user_id=user_id,
            defaults={
                'name': user_info.get('name'),
                'mobile': user_info.get('mobile')
            }
        )
        return feishu_user

    @staticmethod
    def get_all_feishu_users():
        return FeishuUser.objects.all()

    @staticmethod
    def create_feishu_group(name, user_ids):
        chat_id = FeishuAPI.create_group(name, user_ids)
        return chat_id

    @staticmethod
    def send_message_to_group(chat_id, message):
        message_id = FeishuAPI.send_message(chat_id, message)
        return message_id

    @staticmethod
    def some_internal_function(chat_id, form_link):
        # 生成消息卡片JSON
        card_json = generate_reminder_card(form_link)

        # 调用内部函数发送消息并置顶
        result = FeishuAPI.send_and_pin_message(chat_id, card_json)
        return result

    def reminder_task(participants, reminder_frequency, form_link):
        global participants_list
        participants_list = participants[:]
        chat_id = FeishuService.create_feishu_group(participants)
        card_json = generate_reminder_card(form_link)
        FeishuAPI.send_and_pin_message(chat_id, card_json)

        def reminder():
            while participants_list:
                for participant in participants_list:
                    try:
                        FeishuAPI.send_message_with_mention(chat_id, reminder_frequency, participant)
                    except Exception as e:
                        print(f"Failed to send reminder: {e}")
                threading.Timer(reminder_frequency * 60, reminder).start()
                break

        if participants_list:
            reminder()



    def handle_callback(request):
        global participants_list
        user_id = request.data.get('open_id')
        if user_id in participants_list:
            participants_list.remove(user_id)
        return {"message": "Callback received and processed successfully"}