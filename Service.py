
try:
    from android import AndroidService
except:
    Service = None


class CurlService(AndroidService):
    pass