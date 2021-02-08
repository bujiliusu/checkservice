import requests


svc_list = ("bigtree-auth",
"bigtree-sign",
"bigtree-mq",
"qsls-limit",
"bigtree-invoice",
"bigtree-gateway",
"qsls-expense",
"bigtree-credit",
"bigtree-system",
"bigtree-message",
"qsls-batch",
"qsls-cst",
"bigtree-front",
"qsls-back",
"bigtree-scfp",
"bigtree-workflow",
"bigtree-event",
"qsls-client",
"qsls-finance",
"qsls-front",
"bigtree-file",
"qsls-postloan",
"qsls-receivable",
"qsls-app",
"bigtree-pay",
"test1",
"test2")

def get_svc_info(svc_list):
    url = 'http://spboot.bigtreefinance.com:8080/admin/applications'
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


def post_dingTaik(message):
    # https
    url = "https://oapi.dingtalk.com/robot/send?access_token=f8e5c0d09f615101e6067428996af309ec3cbdbd20d31a8cb241b4fb8995f4a2"

    content = {
        "msgtype": "text",
        "text": {
            "content": message
        },
        "at": {
            # @电话某人
            #"atMobiles": [
            #   "156xxxx8827",
            #    "189xxxx8325"
            #],
            # 是否@所有人
            "isAtAll": False
        }
    }
    # 编码utf-8
    headers = {"Content-Type": "application/json;charset=utf-8"}

    r = requests.post(url=url, headers=headers, json=content)

if __name__ == '__main__':
    svc_info_list = get_svc_info(svc_list)
    message = ""
    for svc_info in svc_info_list:
        if svc_info.get('status') != 'UP':
            message += svc_info.get('name') + "服务异常，请登录服务器检查\n"
    message = message if message else "所有服务正常"
    #print(message)

    post_dingTaik(message)
