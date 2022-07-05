class BaseConfig(object):
    URL = 'http://spboot.bigtreefinance.com/admin/applications'
    RISK_URL = 'https://risk.bigtreefinance.com/api/management/error'
    APP_SECRET = '0UC8fpFH9sUGww7_b8AjNmmLwEPl6u7b-NyWoezr1gUQfwH3bslOXp5C4znxC4c_'
    NACOS = 'https://nacos.k6.bigtree.tech/nacos/v1/ns/catalog/services?hasIpCount=true&withInstances=false&pageNo=1&pageSize=100&serviceNameParam=&groupNameParam=&accessToken={}&namespaceId=btfdp'
    RX_NACOS = 'http://nacos.btrx.k6.bigtree.tech/nacos/v1/ns/catalog/services?hasIpCount=true&withInstances=false&pageNo=1&pageSize=100&serviceNameParam=&groupNameParam=&accessToken={}&namespaceId=btrx'
    SCV_LIST = ("bigtree-audit",
                "bigtree-auth",
                "bigtree-credit",
                "bigtree-event",
                "bigtree-file",
                "bigtree-front",
                "bigtree-gateway",
                "bigtree-invoice",
                "bigtree-message",
                "bigtree-mq",
                "bigtree-pay",
                "bigtree-questionnaire",
                "bigtree-scfp",
                "bigtree-sign",
                "bigtree-system",
                "bigtree-workflow",
                "qsls-app",
                "qsls-back",
                "qsls-batch",
                "qsls-channel",
                "qsls-client",
                "qsls-cst",
                "qsls-expense",
                "qsls-finance",
                "qsls-front",
                "qsls-fund",
                "qsls-limit",
                "qsls-postloan",
                "qsls-receivable",
                "qsls-referee"
                )
    NACOS_LIST = ("fund-platform",
                  "fund-batch",
                  "datawarehouse-platform",
                  "bigtree-file",
                  "fund-gateway",
                  "bigtree-system",
                  "bigtree-message-nacos",
                  "fund-bank-wh",
                  "fund-bank-qs",
                  "fund-bank-xiaowei",
                  "fund-payment-unionpay"
                  )


    RX_NACOS_LIST = ("rx-job-admin",
                     "rx-gateway",
                     "rx-sign",
                     "rx-customer",
                     "rx-app",
                     "rx-back",
                     "rx-system",
                     "rx-auth",
                     "rx-message",
                     "rx-file"
                     )
    NICK_LIST = ("苏合信", "常蒙蒙")

class APSchedulerJobConfig(BaseConfig):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    MYTOKEN = 'f8e5c0d09f615101e6067428996af309ec3cbdbd20d31a8cb241b4fb8995f4a2'
    TOKEN = 'ddaa188cf6d31915cd653d54538bd3d8bdc88d9b48a4e6ed4cdcf2e9f7dbd300'

    JOBS = [
        {
            'id': 'No1',
            'func': 'app:check_service',
            'args': '',
            'trigger': {
                'type': 'cron',
                'day_of_week': 'mon-sun',
                'hour': '13, 22',
                'minute': '10'
            }
        }
    ]
