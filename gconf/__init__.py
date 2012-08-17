import os
import pkgutil
from collections import namedtuple


class Url(namedtuple("Url", "url data post cookie")):
    def __new__(cls, url, data=[], post=False, cookie=[]):
        # add default values
        return super(Url, cls).__new__(cls, url, data, post, cookie)

Proxy = namedtuple("Proxy", "address type")


class Hello(object):
    def __init__(self, string):
        pass

useragents = [
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1)",
"Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1",
"Mozilla/5.0 (compatible; MSIE 5.5; Windows NT 5.0; .NET CLR 1.0.3705)",
"Mozilla/5.0 (compatible; Konqueror/2.2.2; Linux 2.4.14-xfs; X11; i686)",
"Mozilla/5.0 (SunOS 5.8 sun4u; U) Opera 5.0 [en]",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/0.2.153.1 Safari/525.19",
"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.1) Gecko/20061205 Iceweasel/2.0.0.1 (Debian-2.0.0.1+dfsg-2)",
"Opera/9.60 (Windows NT 5.1; U; de) Presto/2.1.1",
"Opera/7.x (Windows NT 5.1; U) [en]",
"Opera/9.0 (Windows NT 5.1; U; en)",
]


def handle_content(url, headers, content):
    print url, headers, len(content)


def handle_error(url, e):
    print ("Error #%s" % e.code), url, str(e)


def handle_finish():
    pass

proxies = []
