import json
import datetime
import hashlib
import time
from your_code_here.RedisUtil import RedisUtil
from urllib.parse import quote, unquote
from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__, 
            template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'),
            static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static'))
redis_util = RedisUtil()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    request_data = request.json
    nick = request_data.get('nick', '')
    if not nick:
        return json.dumps({'success': False, 'reason': '昵称为空！'}, ensure_ascii=False)
    #if redis_util.is_nick_already_exists(nick):
        #return json.dumps({'success': False,
                           #'reason': '昵称：{nick}已经被人占用！'.format(nick=nick)}, ensure_ascii=False)

    token = nick + str(time.time())
    token_md5 = hashlib.md5(token.encode()).hexdigest()
    redis_util.set_token(nick, token_md5)
    response = app.make_response(json.dumps({'success': True, 'token': token_md5}))
    response.set_cookie('name', quote(nick, safe=''))
    response.set_cookie('token', token_md5)
    return response


@app.route('/room')
def room():
    nick = request.cookies.get('name', '')
    token = request.cookies.get('token', '')

    nick = unquote(nick)
    saved_token = redis_util.get_token(nick)
    if token == saved_token:
        return render_template('chatroom.html')
    return redirect('/')





@app.route('/post_message', methods=['POST'])
def post_message():
    message = request.json
    print("post_message",message)
    msg = message.get('msg', '')
    nick = message.get('nick', '')
    if not all([msg, nick]):
        return json.dumps({'success': False, 'reason': '昵称或聊天内容为空！'}, ensure_ascii=False)

    expire_time = redis_util.get_nick_msg_expire_time(nick, msg)
    print("expire_time =X ",expire_time)
    if not expire_time:
        message_info = {'msg': message['msg'],
                        'post_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'nick': message['nick']}
        redis_util.push_chat_info(message_info)
        redis_util.set_nick_msg_expire_time(nick, msg)
        print("post_message 3 ",success)
        return json.dumps({'success': True})
    elif expire_time >= 1:
        return json.dumps({'success': False,
                           'reason': '在两分钟内不同发送同样的内容！还剩{expire_time}秒'.format(expire_time=expire_time)},
                          ensure_ascii=False)
    else:
        message_info = {'msg': message['msg'],
                        'post_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'nick': message['nick']}
        redis_util.push_chat_info(message_info)
        redis_util.set_nick_msg_expire_time(nick, msg)
        return json.dumps({'success': True})

@app.route('/get_chat_list')
def get_chat_list():
    chat_list = redis_util.get_chat_list()
    return json.dumps(chat_list, ensure_ascii=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)











