

import requests

# session = requests.Session()
url = 'https://nacos.k5.bigtree.tech/nacos/v1/auth/users/login'
url2 = 'https://nacos.k6.bigtree.tech/nacos/v1/ns/catalog/services?hasIpCount=true&withInstances=false&pageNo=1&pageSize=10&serviceNameParam=&groupNameParam=&accessToken={}&namespaceId=btfdp'

# session.post(url)

my_data = {
        'username': 'nacos',
        'password': 'nacos'
    }
r = requests.post(url, data=my_data)
token = r.json()['accessToken']

r = requests.get(url2.format(token))
print(r.json())

