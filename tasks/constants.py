def generate_reminder_card(form_link):
    return {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "任务提醒"
            }
        },
        "elements": [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"大家记得填表奥，以下为表格链接：[点击这里填写表格]({form_link})"
                }
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "已完成"
                        },
                        "type": "primary",
                        "value": {
                            "type": "confirm"
                        },
                        "action": {
                            "type": "submit",
                            "value": {
                                "callback_key": "task_completed"
                            }
                        }
                    }
                ]
            }
        ]
    }