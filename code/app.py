from flask import Flask, request,abort,make_response
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import base64
import hmac
import json
import hashlib
import time
from datetime import datetime

app = Flask(__name__)
app.config.from_object('settings.APSchedulerJobConfig')
url = app.config['URL']
svc_list = app.config['SCV_LIST']
app_secret = app.config['APP_SECRET']
token = app.config['TOKEN']


def get_git_info():
    ids = ['998', '1004', '1150']
    baseurl = "https://gitlab.bigtree.com/api/v4/projects/{}/merge_requests?state=merged"
    url = "https://gitlab.bigtree.com/api/v4/projects/998/merge_requests?state=merged"
    urls = [ {'id':id, 'url': baseurl.format(id)} for id in ids]
    headr = {
        'private-token': 'gFPx-7R9byeF2wxUhJnS'
    }
    result_info_list = []
    for url in urls:
        result = requests.get(url['url'], headers=headr, verify=False).json()
        result_info = {}
        result_info['id'] = url['id']
        result_info['result'] = result
        result_info_list.append(result_info)
    return result_info_list

def check_service():
    result_info_list = get_git_info()
    for result_info in result_info_list:
        for merge in result_info['result']:
            merged_at_string = merge['merged_at'].split('.')[0]
            merged_at = datetime.strptime(merged_at_string, '%Y-%m-%dT%H:%M:%S')
            target_branch = merge['target_branch']
            title = merge['title']
            title = title + '于' + merged_at_string + 'merge到master，服务健康检查:\n'
            if merged_at.date() == datetime.now().date() and target_branch == "master":
                message = get_svc_info(url, svc_list, title)
                post_ding_git(message)

def get_svc_info(url, svc_list, add_message=''):
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
    message = ""
    for svc_info in svc_info_list:
        if svc_info.get('status') != 'UP':
            message += svc_info.get('name') + "服务异常，请登录服务器检查\n"
    message = message if message else "所有服务正常"
    message = add_message + message
    return message


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
def post_ding_git(content):
    """
    回调信息，即发送给webhook的信息
    :param content:
    :param webhook:
    :return:
    """
    content = content
    global token
    url = "https://oapi.dingtalk.com/robot/send?access_token=" + token
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
        message = get_svc_info(url, svc_list)
        post_ding(message, sessionWebhook)
        headers = {
            "content-type": "text/plain"
        }
        response = make_response("<html></html>, 200")
        response.headers = headers
        return response

if __name__ == "__main__":
    scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0')

