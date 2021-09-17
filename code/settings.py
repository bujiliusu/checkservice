class BaseConfig(object):
    URL = 'http://spboot.bigtreefinance.com/admin/applications'
    APP_SECRET = '0UC8fpFH9sUGww7_b8AjNmmLwEPl6u7b-NyWoezr1gUQfwH3bslOXp5C4znxC4c_'

    SCV_LIST = ("bigtree-auth",
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
