import requests
import base64
import hmac
import json
import hashlib
import time

from flask import Flask, request,abort,make_response


app = Flask(__name__)
app.config.from_object('settings.BaseConfig')
url = app.config['URL']
svc_list = app.config['SCV_LIST']
print(svc_list)
app_secret = app.config['APP_SECRET']

def get_svc_info(url, svc_list):
    url = url
    svc_list = svc_list
    svc_info = {}
    svc_info_list = []

    json_result = requests.get(url).json()

    for svc in svc_list:
        for result in json_result:
            if result.get('name') == svc:
                svc_info = {}
                svc_info['name'] = svc
                svc_info['status'] = result.get('status')
                svc_info_list.append(svc_info)

    result = [svc['name'] for svc in json_result]
    for svc in svc_list:
        if svc not in result:
            svc_info = {}
            svc_info['name'] = svc
            svc_info['status'] = 'DOWN'
            svc_info_list.append(svc_info)
    return svc_info_list


def getsign(app_secret, post_timestamp):
    """
    对POST过来的信息进行鉴权，确认是钉钉机器人发送的
    :param app_secret: 机器人应用的app_secret
    :param post_timestamp: POST信息的时间戳
    :return:
    """
    timestamp = post_timestamp
    app_secret = app_secret
    app_secret_enc = app_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, app_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = base64.b64encode(hmac_code).decode('utf-8')
    return sign
def post_ding(content, webhook):
    """
    回调信息，即发送给webhook的信息
    :param content:
    :param webhook:
    :return:
    """
    content = content
    url = webhook
    body = {
        "msgtype": "text",
        "text": {
            "content": content,
        }
    }
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }

    try:
        requests.adapters.DEFAULT_RETRIES = 2
        result= requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=5)
    except Exception as ee:
        print(ee)

@app.route("/", methods=['GET','POST', 'HEAD'])
def index():
    if request.method == 'GET':
        abort(404)
    if request.method == 'HEAD':
        abort(404)
    if request.method == 'POST':
        post_timestamp = request.headers.get('Timestamp')
        sign = getsign(app_secret, post_timestamp)
        post_sign = request.headers.get('Sign')
        timestamp = str(round(time.time() * 1000))
        if post_sign != sign or abs(int(post_timestamp) - int(timestamp)) > 360000:
            abort(404)

        data = request.json
        sessionWebhook = data.get('sessionWebhook')
        content = data.get('text').get('content')
        content = content.split()
        if len(content) != 2:
            content = '参数错误，实例：check service'
            post_ding(content=content, webhook=sessionWebhook)
            headers = {
                "content-type": "text/plain"
            }
            response = make_response("<html></html>, 200")
            response.headers = headers
            return response

        method = content[0]
        site = content[1]
        if method != "check" or site != "service":
            content = '参数错误，实例：check service'
            post_ding(content=content, webhook=sessionWebhook)
            headers = {
                "content-type": "text/plain"
            }
            response = make_response("<html></html>, 200")
            response.headers = headers
            return response

        svc_info_list = get_svc_info(url, svc_list)
        message = ""
        for svc_info in svc_info_list:
            if svc_info.get('status') != 'UP':
                message += svc_info.get('name') + "服务异常，请登录服务器检查\n"
        message = message if message else "所有服务正常"
        post_ding(message, sessionWebhook)
        headers = {
            "content-type": "text/plain"
        }
        response = make_response("<html></html>, 200")
        response.headers = headers
        return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
