from requests.exceptions import ConnectTimeout


class NotFoundException(Exception):
    message = "资源不存在，或链接无效"


class ServerErrorException(Exception):
    message = "服务器错误"

class TimeoutException(ConnectTimeout):
    message = "解析超时"

class SpecialErrorException(Exception):
    message = "出于某些特殊原因，主要目标资源未能解析"


errors = (
    NotFoundException,
    ServerErrorException,
    TimeoutException,
    SpecialErrorException,
)