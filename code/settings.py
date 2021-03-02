class BaseConfig(object):
    URL = 'http://spboot.bigtreefinance.com:8080/admin/applications'
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
