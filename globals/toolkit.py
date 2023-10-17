from urllib.parse import unquote

def getRequestIP(request):
    return request.get_host()

def getCookieData(request):
    return int(request.COOKIES['rid']), unquote(request.COOKIES['name']), request.COOKIES['psw']