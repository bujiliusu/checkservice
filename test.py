#
#
# import requests
#
# # session = requests.Session()
# url = 'https://nacos.k5.bigtree.tech/nacos/v1/auth/users/login'
# url2 = 'https://nacos.k6.bigtree.tech/nacos/v1/ns/catalog/services?hasIpCount=true&withInstances=false&pageNo=1&pageSize=10&serviceNameParam=&groupNameParam=&accessToken={}&namespaceId=btfdp'
#
# # session.post(url)
#
# my_data = {
#         'username': 'nacos',
#         'password': 'nacos'
#     }
# r = requests.post(url, data=my_data)
# token = r.json()['accessToken']
#
# r = requests.get(url2.format(token))
# print(r.json())
#
#
# url = 'http://spboot.bigtreefinance.com/admin/applications'
# json_result = requests.get(url).json()
#
# print(json_result)

from urllib.parse import urlparse
from urllib.parse import urljoin

def url_to_domain(url):
    o = urlparse(url)
    print(o.scheme)
    print(o.netloc)
    print(o.path)
    print(o.params)
    print(o.query)
    print(o.fragment)
    domain = o.hostname
    return domain

urls = [
    "http://meiwen.me/src/index.html",
    "http://1000chi.com/game/index.html",
    "http://see.xidian.edu.cn/cpp/html/1429.html",
    "https://docs.python.org/2/howto/regex.html",
    """https://www.google.com.hk/search?client=aff-cs-360chromium&hs=TSj&q=url%E8%A7%A3%E6%9E%90%E5%9F%9F%E5%90%8Dre&oq=url%E8%A7%A3%E6%9E%90%E5%9F%9F%E5%90%8Dre&gs_l=serp.3...74418.86867.0.87673.28.25.2.0.0.0.541.2454.2-6j0j1j1.8.0....0...1c.1j4.53.serp..26.2.547.IuHTj4uoyHg""",
    "file:///D:/code/echarts-2.0.3/doc/example/tooltip.html",
    "http://api.mongodb.org/python/current/faq.html#is-pymongo-thread-safe",
    "https://pypi.python.org/pypi/publicsuffix/",
    "http://127.0.0.1:8000",
    "https://nacos.k6.bigtree.tech/nacos/v1/ns/catalog/services?hasIpCount=true&withInstances=false&pageNo=1&pageSize=100&serviceNameParam=&groupNameParam=&accessToken={}&namespaceId=btfdp"
]

# for url in urls:
#     print(url_to_domain(url))

url = "https://nacos.k6.bigtree.tech/nacos/v1/ns/catalog/servi"
base_url = '/nacos/v1/auth/users/login'
domain = url_to_domain(url)
print('*'*20)
print(domain)
domain = 'https://' + domain
login_url = urljoin(domain, base_url)
print(login_url)