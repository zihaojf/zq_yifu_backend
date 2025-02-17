from server.settings.components import config
from server.settings.components.configs import CacheConfig

# debug 模式
DEBUG = config("DJANGO_DEBUG", False, cast=bool)

ALLOWED_HOSTS = [
    "localhost",
    "yifu.ziqiang.net.cn",
    "api.yifu.ziqiang.net.cn",
    "test.yifu.ziqiang.net.cn",
    "api.test.yifu.ziqiang.net.cn",
]

SERVER_URL = config("SERVER_URL", "https://api.yifu.ziqiang.net.cn")

# region Cache
# Redis
CacheConfig.url = "redis://redis"
CACHES = CacheConfig.get()
# endregion
