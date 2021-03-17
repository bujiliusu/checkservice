import requests
import json
def get_svc_info(url, svc_list, add_message=''):
    url = url
    svc_list = svc_list
    svc_info = {}
    svc_info_list = []
    print(requests.get(url))
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
    post_ding(message, url)
def post_ding(message, url):
    print('lllll')
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
                "bigtree-pay"
                )
url = 'http://115.182.11.70:8080/admin/applications'

# get_svc_info(url, svc_list)

aaa = "http://spboot.bigtreefinance.com"

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

# result_info_list = get_git_info()
# print(json.dumps(result_info_list[0], indent=4))

from datetime import datetime,date
time1 = "2021-02-26T13:11:10"
d = date.today()
# print(d.year)
# print(d.isoformat())
# print(d.strftime('%Y/%m/%d'))
time2 = datetime.strptime(time1, '%Y-%m-%dT%H:%M:%S')
print(time2, type(time2))
print(time2.hour, type(time2.hour))
print(time2.min, type(time2.min))
# if time2.hour >= 13 and time2.min >= 10:
#     print('sucess')

string2 = "2021-02-26 13:10:0134"
a = string2.split()
print(a)
if a[1] > '13:10:00':
    print('sucess')
if time2.hour == 13:
    print(time2.date())
print(datetime.now().hour, type(datetime.now().hour))

for i in range(0, 10):
    for j in range(0, 10):

        if j == 5:
            continue
        print(i, j)