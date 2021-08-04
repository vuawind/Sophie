import os
import calendar, time 
import datetime
from slack_bolt import App, Ack
from slack import WebClient
import json
import random
import string
import pandas as pd
from frame import *

app = App(
    signing_secret = os.environ.get("SLACK_SIGN"),

# Initialize a Web API client
    token=os.environ.get("SLACK_BOT_TOKEN")
)

def write_json(new_data,section, filename):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        if section not in file_data:
            file_data.update(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def write_json_option(new_data,section,num, filename='question.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        if new_data not in file_data[section][num]["elements"][0]["options"]:
            file_data[section][num]["elements"][0]["options"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

def wow():
    xl=pd.ExcelFile('chatbot.xlsx')
    sheets_numb = len(xl.sheet_names)
    home_tab = {
        "WELCOME_BLOCK": home()
    }
    write_json(home_tab,"WELCOME_BLOCK",'home.json')
    for i in range(sheets_numb):
        data = pd.read_excel('chatbot.xlsx',sheet_name=i)
        dictionary = {
            xl.sheet_names[i]: question_block(xl.sheet_names[i],"block","select")
        }
        buttonchoose = headers(xl.sheet_names[i],f"value-{i}")
        write_json(dictionary,xl.sheet_names[i],'question.json')
        write_json_option(buttonchoose,"WELCOME_BLOCK",0,'home.json')
        df=pd.DataFrame(data, columns= ['questions','answers'])
        for j in range(len(df.index)):
            write_json_option(option_block(df.iloc[j]['questions'],f"value-{j}"),xl.sheet_names[i],1,'question.json')

    other_block = {
        "Other/Câu hỏi khác": other()
    }
    write_json_option(headers("Other/Câu hỏi khác","other"),"WELCOME_BLOCK",0,'home.json')
    write_json(other_block,"Other/Câu hỏi khác",'question.json')

@app.shortcut("sophie")
def sophie(event, say, ack, client,shortcut, body):
    ack()
    with open('home.json','r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        client.chat_postMessage(channel=shortcut['user']['id'], text=f":hugging_face: Xin chào <@{body['user']['id']}>, Tôi là Sophie - HR Helpdesk. Bạn có câu hỏi nào cho Sophie - Hãy bấm vào mục liên quan bên dưới nhé!")
        client.chat_postMessage(channel=shortcut['user']['id'], blocks=file_data["WELCOME_BLOCK"])

@app.action("action_id")
def onboard(event, say, ack, client,body,action):
    ack()
    with open('question.json','r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        title = action["selected_option"]["text"]["text"]
        client.chat_postMessage(channel=body['user']['id'], blocks=file_data[title])

@app.action("select")
def onboard(event, say, ack, client,body,action):
    header=body['message']['blocks'][0]['text']['text']
    val=action["selected_option"]["value"]
    value=int(val[6:])
    data = pd.read_excel('chatbot.xlsx',sheet_name=header)
    df=pd.DataFrame(data, columns=['answers'])
    ack()
    new=df.iloc[value]['answers'].replace(r'\n', '\n')
    client.chat_postMessage(channel=body['user']['id'], text=f"{new}")

@app.action("back")
def back(event, say, ack, client,body,action):
    ack()
    with open('home.json','r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        client.chat_postMessage(channel=body['user']['id'], text=f":hugging_face: Xin chào <@{body['user']['id']}>, Tôi là Sophie - HR Helpdesk. Bạn có câu hỏi nào cho Sophie - Hãy bấm vào mục liên quan bên dưới nhé!")
        client.chat_postMessage(channel=body['user']['id'], blocks=file_data["WELCOME_BLOCK"])

@app.event("team_join")
def ask_for_introduction(event, say, client, body):
    day2 = datetime.datetime.today() + datetime.timedelta(days=1)
    day3 = datetime.datetime.today() + datetime.timedelta(days=2)
    scheduled_time = datetime.time(hour=9, minute=30, second=10)
    schedule_timestamp1 = datetime.datetime.combine(day2, scheduled_time).strftime('%s')
    schedule_timestamp2 = datetime.datetime.combine(day3, scheduled_time).strftime('%s')
    user_id = event["user"]['id']
    text2 = f"hugging_face: Xin chào, <@{user_id}> là nhân viên mới đúng không? Hãy hỏi Sophie những điều thắc mắc nhé! (bằng cách bấm vào mục liên quan bên dưới nhé)"
    say(text=text2, channel=user_id)
    client.chat_postMessage(channel=user_id, blocks=welcome.WELCOME_BLOCK)
    client.chat_scheduleMessage(channel=user_id,text=f"Xin chào, ngày hôm nay của bạn thế nào? Bạn lưu ý hoàn thành các khóa học E-Learning - Đào tạo hội nhập trong 3 ngày từ ngày gia nhập và Hoàn thiện hồ sơ nhân sự trước 29 nhé. Có thắc mắc khác hãy hỏi Sophie! Chúc bạn luôn vui, khỏe! :grin:", blocks=welcome.WELCOME_BLOCK, post_at=schedule_timestamp1)
    client.chat_scheduleMessage(channel=user_id,text=f"Xin chào, Bạn đã nghe về 1office? Hmm. Ngày công trên 1office được dùng để tính lương cho chính bạn. Hãy truy cập ngay, kiểm tra và tạo ngày công chính xác để nhận đủ lương tháng. Lưu ý hệ thống chỉ cho phép tạo trong vòng 5 ngày, do đó, bạn cần kiểm tra hàng ngày nhé. Nếu không rõ cách làm, hãy bấm vào mục VII. CHẤM CÔNG - TÍNH LƯƠNG để Sophie hướng dẫn bạn! :v:", blocks=welcome.WELCOME_BLOCK, post_at=schedule_timestamp2)

@app.action("submit")
def other_text(event, say, ack, client,body,action,button):
    text = body['state']['values']['block_h']['other_input']['value']
    ts = body['message']['ts']
    ack()
    #Nếu như channel của HR đổi thì lấy ID của channel mới rồi thay vào
    client.chat_postMessage(channel = 'C025751TS0P', text = f"You have a new question from <@{body['user']['id']}>:\n:point_right: {text}")
    client.chat_update(ts=ts, channel = body['container']['channel_id'], blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Gửi câu hỏi thành công.\nCảm ơn bạn. Phòng Nhân sự sẽ phản hồi bạn trong thời gian sớm nhất!"
			}
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
	])

def delete_json():
    jsonFile = open("home.json", "w+")
    jsonFile.write(json.dumps({}))
    jsonFile = open("question.json", "w+")
    jsonFile.write(json.dumps({}))

if __name__ == "__main__":
    delete_json()
    wow()
    app.start(port=int(os.environ.get("PORT", 8000)))
