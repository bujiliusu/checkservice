from flask import Flask, request,abort,make_response
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_ALL
from apscheduler.events import SchedulerEvent
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import base64
import hmac
import json
import hashlib
import time
from datetime import datetime, timedelta
import logging
from urllib.parse import urlparse
from urllib.parse import urljoin
logging.getLogger().setLevel(logging.INFO)

app = Flask(__name__)
app.config.from_object('settings.APSchedulerJobConfig')
url = app.config['URL']
risk_url = app.config['RISK_URL']
svc_list = app.config['SCV_LIST']
app_secret = app.config['APP_SECRET']
token = app.config['TOKEN']
mytoken = app.config['MYTOKEN']
rxtoken = app.config['RXTOKEN']
nick_list = app.config['NICK_LIST']
nacos = app.config['NACOS']
rx_nacos = app.config['RX_NACOS']
dyy_nacos = app.config['DYY_NACOS']
ifbc_nacos = app.config['IFBC_NACOS']
nacos_list = app.config['NACOS_LIST']
rx_nacos_list = app.config['RX_NACOS_LIST']
dyy_nacos_list = app.config['DYY_NACOS_LIST']
ifbc_nacos_list = app.config['IFBC_NACOS_LIST']


def get_git_info():
    ids = ['20', '19', '23', '26', '244', '387', '292']
    baseurl = "https://git.int.bigtree.tech/api/v4/projects/{}/merge_requests?state=merged&target_branch=master"
    urls = [ {'id':id, 'url': baseurl.format(id)} for id in ids]
    headr = {
        'private-token': 'iz7zm_TLxn4isA1eMn_D'
    }
    result_info_list = []
    for url in urls:
        result = requests.get(url['url'], headers=headr, verify=False).json()
        result_info = {}
        result_info['id'] = url['id']
        result_info['result'] = result
        result_info_list.append(result_info)
    return result_info_list

def check_service(env='pro'):
    global token
    global rxtoken
    message = ''
    messageAll = ''
    result_info_list = get_git_info()
    for result_info in result_info_list:
        for merge in result_info['result']:
            merged_at_string = merge['merged_at'].split('.')[0]
            merged_at = datetime.strptime(merged_at_string, '%Y-%m-%dT%H:%M:%S')
            merged_at = merged_at + timedelta(hours=8)
            merged_at_string = merged_at.strftime("%Y-%m-%d %H:%M:%S")
            target_branch = merge['target_branch']
            if merged_at.date() == datetime.now().date():
                if datetime.now().hour == 22:
                    if merged_at_string.split()[1] <= '13:15:00':
                        continue
                title = merge['title']
                if result_info['id'] == '20':
                    name = 'bigtree-deploy'
                if result_info['id'] == '19':
                    name = 'qsls-deploy'
                if result_info['id'] == '23':
                    name = 'fdp-deploy'
                if result_info['id'] == '26':
                    name = 'risk-deploy'
                if result_info['id'] == '244':
                    name = 'rx-deploy'
                if result_info['id'] == '387':
                    name = 'dyy-deploy'
                if result_info['id'] == '292':
                    name = 'ifbc-deploy'
                title = name + '-' + title + '，已完成上线。' + '服务健康检查:\n'
                if name == 'fdp-deploy':
                    message = get_nacos_info(nacos, nacos_list, title)
                elif name == 'rx-deploy':
                    message = get_nacos_info(rx_nacos, rx_nacos_list, title)
                elif name == 'dyy-deploy':
                    message = get_nacos_info(dyy_nacos, dyy_nacos_list, title)
                elif name == 'ifbc-deploy':
                    message = get_nacos_info(ifbc_nacos, ifbc_nacos_list, title)
                elif name == 'risk-deploy':
                    message = get_risk_info(title)
                else:
                    message = get_svc_info(url, svc_list, title)
                if env == 'pro':
                    logging.info(message)
                    if name == 'rx-deploy' or name == 'dyy-deploy' or name == 'ifbc-deploy':
                        post_ding_pro(message, rxtoken)
                    else:
                        post_ding_pro(message, token)
                if env == 'dev':
                    messageAll = messageAll + message + '\n'
    if env == 'dev':
        if messageAll == '':
            messageAll = '今日无上线\n'
            title = '服务健康检查:\n'
            text_bt_qsls = get_svc_info(url, svc_list)
            text_fdp = get_nacos_info(nacos, nacos_list)
            text_rx = get_nacos_info(rx_nacos, rx_nacos_list)
            text_dyy = get_nacos_info(dyy_nacos, dyy_nacos_list)
            text_ifbc = get_nacos_info(ifbc_nacos, ifbc_nacos_list)
            text_risk = get_risk_info()
            text_bt_qsls = text_bt_qsls if text_bt_qsls != '所有服务正常' else ''
            text_fdp = text_fdp if text_fdp != '所有服务正常' else ''
            text_rx = text_rx if text_rx != '所有服务正常' else ''
            text_dyy = text_dyy if text_rx != '所有服务正常' else ''
            text_ifbc = text_ifbc if text_rx != '所有服务正常' else ''
            text_risk = text_risk if text_risk != '所有服务正常' else ''
            if text_fdp == '' and text_bt_qsls == '' and text_risk == '' and text_rx == '' and text_dyy == '' and text_ifbc == '':
                text = '所有服务正常'
            else:
                text = text_bt_qsls + '\n' + text_fdp + '\n' + text_risk + '\n' + text_rx + '\n' + text_dyy + '\n' + text_ifbc
                text = text.lstrip()
            messageAll = messageAll + text + '\n'
        logging.info(messageAll)
        post_ding_test(messageAll)

# def check_service_test():
#     result_info_list = get_git_info()
#     message = ''
#     for result_info in result_info_list:
#         for merge in result_info['result']:
#             merged_at_string = merge['merged_at'].split('.')[0]
#             merged_at = datetime.strptime(merged_at_string, '%Y-%m-%dT%H:%M:%S')
#             merged_at = merged_at + timedelta(hours=8)
#             merged_at_string = merged_at.strftime("%Y-%m-%d %H:%M:%S")
#             target_branch = merge['target_branch']
#             if merged_at.date() == datetime.now().date() and target_branch == "master":
#                 if datetime.now().hour == 22:
#                     if merged_at_string.split()[1] <= '13:10:00':
#                         continue
#                 title = merge['title']
#                 if result_info['id'] == '20':
#                     name = 'bigtree-deploy'
#                 if result_info['id'] == '19':
#                     name = 'qsls-deploy'
#                 if result_info['id'] == '23':
#                     name = 'fdp-deploy'
#                 if result_info['id'] == '26':
#                     name = 'risk-deploy'
#                 if result_info['id'] == '244':
#                     name = 'rx-deploy'
#                 title = name + '-' + title + '，已完成上线。' + '服务健康检查:\n'
#                 if name == 'fdp-deploy':
#                     text = get_nacos_info(nacos, nacos_list, title)
#                 elif name == 'rx-deploy':
#                     message = get_nacos_info(rx_nacos, rx_nacos_list, title)
#                 elif name == 'risk-deploy':
#                     text = get_risk_info(title)
#                 else:
#                     text = get_svc_info(url, svc_list, title)
#                 message = message + text + '\n'
#     if message == '':
#         message = '今日无上线\n'
#         title = '服务健康检查:\n'
#         text_bt_qsls = get_svc_info(url, svc_list)
#         text_fdp = get_nacos_info(nacos, nacos_list)
#         text_rx = get_nacos_info(rx_nacos, rx_nacos_list)
#         text_risk = get_risk_info()
#         text_bt_qsls = text_bt_qsls if text_bt_qsls != '所有服务正常' else ''
#         text_fdp = text_fdp if text_fdp != '所有服务正常' else ''
#         text_rx = text_rx if text_rx != '所有服务正常' else ''
#         text_risk = text_risk if text_risk != '所有服务正常' else ''
#         if text_fdp == '' and text_bt_qsls == '' and text_risk == '' and text_rx == '':
#             text = '所有服务正常'
#         else:
#             text = text_bt_qsls + '\n' + text_fdp + '\n' + text_risk + '\n' + text_rx
#             text = text.lstrip()
#         message = message + text + '\n'
#     logging.info(message)
#     post_ding_test(message)

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

    result = [svc['name'] for svc in svc_info_list]
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

def url_to_domain(url):
    o = urlparse(url)
    domain = o.hostname
    return domain


def get_nacos_info(url, svc_list, add_message=''):
    base_url = '/nacos/v1/auth/users/login'
    domain = 'http://' + url_to_domain(url)
    login_url = urljoin(domain, base_url)
    payload =  {
        'username': 'nacos',
        'password': 'nacos'
    }
    r = requests.post(login_url, data=payload)
    nacos_token = r.json()['accessToken']

    url = url
    url = url.format(nacos_token)
    svc_list = svc_list
    svc_info = {}
    svc_info_list = []

    json_result_ori = requests.get(url).json()
    json_result = json_result_ori['serviceList']
    count = json_result_ori['count']

    for svc in svc_list:
        for result in json_result:
            if result.get('name') == svc:
                svc_info = {}
                svc_info['name'] = svc
                svc_info['healthyInstanceCount'] = result.get('healthyInstanceCount')
                svc_info_list.append(svc_info)
    result = [svc['name'] for svc in json_result]
    for svc in svc_list:
        if svc not in result:
            svc_info = {}
            svc_info['name'] = svc
            svc_info['healthyInstanceCount'] = 0
            svc_info_list.append(svc_info)
    message = ""
    for svc_info in svc_info_list:
        if svc_info.get('healthyInstanceCount') < 1:
            message += svc_info.get('name') + "服务异常，请登录服务器检查\n"
    message = message if message else "所有服务正常"
    message = add_message + message
    return message

def get_risk_info(add_message=''):
    message = ""
    code = requests.get(risk_url).status_code
    if code != 200:
        message = "风控系统服务异常，请登录服务器检查\n"
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
def post_ding_test(content):

    content = content
    global mytoken
    myurl = "https://oapi.dingtalk.com/robot/send?access_token=" + mytoken
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
        myresult= requests.post(myurl, data=json.dumps(body), headers=headers, verify=False, timeout=5)
        logging.info(myresult.text)
    except Exception as ee:
        print(ee)

def post_ding_pro(content, token):
    content = content
    token = token
    global mytoken
    url = "https://oapi.dingtalk.com/robot/send?access_token=" + token
    myurl = "https://oapi.dingtalk.com/robot/send?access_token=" + mytoken
    body = {
        "msgtype": "text",
        "text": {
            "content": content,
        }
    }
    body_test = {
        "msgtype": "text",
        "text": {
            "content": content,
        },
        "at": {
            "atMobiles": [
                "18501257410"
            ],
            "isAtAll": False
        }
    }
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
    }

    try:
        requests.adapters.DEFAULT_RETRIES = 2
        result= requests.post(url, data=json.dumps(body), headers=headers, verify=False, timeout=5)
        if content.find('服务异常，请登录服务器检查') != -1:
            myresult= requests.post(myurl, data=json.dumps(body_test), headers=headers, verify=False, timeout=5)
        else:
            myresult = requests.post(myurl, data=json.dumps(body), headers=headers, verify=False, timeout=5)
        logging.info(result.text)
        logging.info(myresult.text)
    except Exception as ee:
        print(ee)

def my_listener(event: SchedulerEvent):

    time_now = datetime.now()
    print("starting cron at", time_now, event.code)

@app.errorhandler(404)
def page_not_found(e):
    return '', 404, {'Server': 'nginx'}
@app.errorhandler(500)
def page_not_found(e):
    return '', 500, {'Server': 'nginx'}

@app.route("/", methods=['GET','POST', 'HEAD'])
def index():
    if request.method == 'GET':
        return '', 404, {'Server': 'nginx'}
    if request.method == 'HEAD':
        return '', 404, {'Server': 'nginx'}
    if request.method == 'POST':
        post_timestamp = request.headers.get('Timestamp')
        sign = getsign(app_secret, post_timestamp)
        post_sign = request.headers.get('Sign')
        timestamp = str(round(time.time() * 1000))
        if post_sign != sign or abs(int(post_timestamp) - int(timestamp)) > 360000:
            return '', 404, {'Server': 'nginx'}

        data = request.json
        senderNick = data.get('senderNick')
        if senderNick in nick_list:
            content = data.get('text').get('content').strip()
            if content == 'check':
                print(content)
                text = "主动检查服务健康状态，结果发送测试群：check dev，结果发送测试与业务群：check pro"
                post_ding_test(text)
            if content == 'check dev':
                check_service('dev')
            if content == 'check pro':
                check_service('pro')

        headers = {
            "content-type": "text/plain"
        }
        response = make_response("<html></html>, 200")
        response.headers = headers
        return response

if __name__ == "__main__":
    scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
    scheduler.add_listener(my_listener, EVENT_ALL)
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0')

