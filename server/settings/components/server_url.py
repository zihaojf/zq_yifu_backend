from server.settings.util import config

SERVER_URL = config("SERVER_URL", "http://localhost:8000")  # 服务器地址

PRODUCTION_SERVER_LIST = [  # 生产服务器列表
    "https://api.yifu.ziqiang.net.cn",
]

DEVELOPMENT_SERVER_LIST = [  # 开发服务器列表
    "http://localhost:8000",
    "https://api.test.yifu.ziqiang.net.cn",
]
