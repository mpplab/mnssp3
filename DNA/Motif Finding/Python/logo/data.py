from urllib.request import urlopen
from urllib.parse import urlencode

def getDiabeticRetinopathyImgaesData(count):
    url = 'http://47.93.227.138/index.php/index/drd/get_trains'
    data = {'count': str(count)}
    s = urlencode(data)
    res = urlopen(url, s.encode())  # post请求
    return res.read().decode()