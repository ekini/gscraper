import gconf
from gconf import Url

def urls_generator():
    for n in xrange(10):
        yield Url("http://vepomsk.ru/"+str(n),  [("var", "value")], False)

urls = urls_generator()

