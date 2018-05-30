from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)
import random
app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('lGimQVoA3W0s9EZ8fMiOJsRtA0b0P+wPY5i098AIoMdYsnN4U+ykPc+a2BDkmczqjttLhNBNhkYTAgQqY15tuQtdXJt8ZEaxhIDW1glP9Mmrwjs04n9wiQQ1xzjx7VbX1eDeWXNlwb+wFyJvOQGy/AdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('66590a1d08a6fabc1adaa2fec8c8a4b5')
gossiping_array = []
c_chat_array = []
beauty_array = []
# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'



def process_condition(temp_array, condition_word):
    process_condition_result = ""
    print("temp_array:"+temp_array[0])
    if(condition_word=="最熱門"):
        process_condition_result = temp_array[0]
    elif(condition_word=="熱門"):
        index = random.randint(0,50)
        process_condition_result = temp_array[index]
    else:
        for i in temp_array:
            if(i['article_title'].find(condition_word) > -1):
                process_condition_result = i
                break    
    return process_condition_result
def process_post(temp_array):
    post_message = ""
    if(temp_array != ""):
        title = temp_array['article_title']
        content = temp_array['content']
        url = temp_array['url']
        post_message = "標題: "+title+"\n內容: "+content+"\n原文網址: "+url
    else:
        post_message = "GG  沒有找到你要的內容"
    return post_message

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):  
    user_message = event.message.text
    user_message = user_message.split()
    respond_message = ""
    if(len(user_message)==1):
        user_message.append("最熱門")
    condition_word = user_message[1]
    if(user_message[0]=="八卦版"):
        gossiping_array = ptt_json("Gossiping")
        result = process_condition(gossiping_array, condition_word)
        result = process_post(result)
        respond_message = TextSendMessage(result)
    elif(user_message[0]=="西洽版"):
        c_chat_array = ptt_json("C_Chat")
        result = process_condition(c_chat_array, condition_word)
        result = process_post(result)
        respond_message = TextSendMessage(result)
    elif(user_message[0]=="表特版"):
        beauty_array = ptt_json("Beauty")
        result = process_condition(beauty_array, condition_word)
        result = process_post(result)
        respond_message = TextSendMessage(result)        
    else:
        method_message = "歡迎使用PTT Line Bot，使用方法為:\n看板名稱(僅支持 八卦版 西洽版 表特版) + 條件\n條件可以是:\"最熱門\"(討論最高) / \"熱門\"(隨機前幾名) / \"關鍵字(標題的)\"\nEX: 八卦版(默認為最熱門) / 八卦版 最熱門 / 西洽版 熱門 / 表特版 學生"
        respond_message = TextSendMessage(method_message)

    line_bot_api.reply_message(
        event.reply_token,
        respond_message)
def ptt_json(path):
    files= os.listdir(path) #得到文件夹下的所有文件名称   
    temp_array = []
    for file in files: #遍历文件夹
        if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开  
            with open(path+"/"+file , 'r',encoding = 'utf8') as reader:
                jf = json.loads(reader.read())
                for j in jf:
                    try:
                        if((j['article_title'].find("公告")==-1) and (len(j['article_title'])>0)):
                            j['message_count']['push'] = int(j['message_count']['push'])
                            temp_array.append(j)
                        else:
                            print("處理公告"+j['article_title'])
                    except :
                        i=0
    temp_array_sorted = sorted(temp_array , key=lambda x:x['message_count']['push'], reverse=True)
    return temp_array_sorted  
import os
import json
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


    
    


