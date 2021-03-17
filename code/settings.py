class BaseConfig(object):
    URL = 'http://spboot.bigtreefinance.com:8080/admin/applications'
    # APP_SECRET = '3yCIyIjvAnvpokzZrrS2RC4M6TGVU4IsliouUot8PIktvRVPTrSSrueyzdb2vSTe'
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

class APSchedulerJobConfig(BaseConfig):
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    # TOKEN = 'a2b9cd66a38b8df3a5512b63ce116913f02c6246ebd5e5a9a39f132abad936d4'
    # TOKEN = '6fa39fc3d312d72a4b0c10064d4d13c04e6aaf634a30b75cc6bdcc0390528cf2'
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
