def question_block(title,block_id,select):
    block = [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": f"{title}"
			}
		},
		{
			"type": "actions",
            "block_id": f"{block_id}",
			"elements":[
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Tìm các câu hỏi tại đây",
						"emoji": True
					},
					"options": [],
					"action_id": f"{select}"
				}
            ]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				}
			]
		},
		{
			"type": "divider"
		}
    ]
    return block

def option_block(question,value):
    block = {
        "text": {
            "type": "plain_text",
            "text": f"{question}",
            "emoji": True
        },
        "value": f"{value}"
    }
    return block

def headers(title,value):
	block = {
		"text": {
			"type": "plain_text",
			"text": f"{title}",
			"emoji": True
		},
		"value": f"{value}"
	}
	return block

def home():
	block = [
        {
            "type": "actions",
            "elements": [
                {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Tìm các mục tại đây",
                        "emoji": True
                    },
                    "options": [],
                    "action_id": "action_id"
                }
            ]
        },
        {
            "type": "divider"
        }
    ]
	return block

def other():
	block = [
		{
			"type": "input",
            "label": {
                "type": "plain_text",
                "text": "Câu hỏi khác",
                "emoji": True
            },
            "block_id": "block_h",
			"element": {
                "type": "plain_text_input",
                "multiline": True,
                "placeholder": {
                    "type": "plain_text",
                    "text": "Câu hỏi này sẽ được gửi đến HR",
                    "emoji": True
                },
                "action_id": "other_input"
            }
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Back/Quay lại",
						"emoji": True
					},
					"value": "click_back",
					"action_id": "back"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Submit/Nộp",
						"emoji": True
					},
					"value": "click_submit",
					"action_id": "submit"
				}
			]
		},
		{
			"type": "divider"
		}
    ]
	return block