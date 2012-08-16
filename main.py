#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: 2012, Eugene "ekini" Dementiev
# Author: Eugene "ekini" Dementiev (http://dementiev.eu)
# License: Beerware

import pkgutil
import argparse

import gevent
from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()

import gconf
import random
import urllib2
import urllib
import logging
from collections import namedtuple
from itertools import imap, cycle, islice

__version__ = "v.0.1"

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def validate_module(m):
    """Validates module by checking variables and callback function"""

    logging.debug("Validating module %r" % m)
    # checks if module has variable 'urls' and it's a dict
    if not hasattr(m, "urls"):
        logging.debug("Variable 'urls' doesn't exist "
                      "in module %r" % m.__name__)
        return False

    # check for handle_content function
    if not hasattr(m, "handle_content"):
        logging.info("Module %r doesn't have 'handle_content' function, "
                     "using dummy print" % m.__name__)
        m.handle_content = gconf.handle_content
    else:
        logging.debug("Module %r has 'handle_content' function, "
                      "checking if it's callable..." % m.__name__)
        if not callable(m.handle_content):
            logging.info("Function 'handle_content' from module %r "
                         "is not callable" % m.__name__)
            return False

    if not hasattr(m, "handle_error"):
        logging.info("Module %r doesn't have 'handle_error' function, "
                     "using dummy" % m.__name__)
        m.handle_error = gconf.handle_error
    else:
        logging.debug("Module %r has 'handle_error' function, "
                      "checking if it's callable..." % m.__name__)
        if not callable(m.handle_error):
            logging.info("Function 'handle_error' from module %r "
                         "is not callable" % m.__name__)
            return False

    if not hasattr(m, "handle_finish"):
        logging.info("Module %r doesn't have 'handle_finish' function, "
                     "using dummy" % m.__name__)
        m.handle_finish = gconf.handle_finish
    else:
        logging.debug("Module %r has 'handle_finish' function, "
                      "checking if it's callable..." % m.__name__)
        if not callable(m.handle_finish):
            logging.info("Function 'handle_finish' from module %r "
                         "is not callable" % m.__name__)
            return False

    if not hasattr(m, "useragents"):
        logging.info("Module %r doesn't have 'useragents' var, "
                     "using default" % m.__name__)
        m.useragents = gconf.useragents
    else:
        logging.debug("Module %r has var 'useragents', "
                      "checking type..." % m.__name__)
        if not isinstance(m.useragents, list):
            logging.info("Variable 'useragents' is not a list")
            return False

    if not hasattr(m, "proxies"):
        logging.info("Module %r doesn't have 'proxies' var, "
                     "using default" % m.__name__)
        m.proxies = list(gconf.proxies)
    else:
        logging.debug("Module %r has var 'proxies', "
                      "checking type..." % m.__name__)
        if not isinstance(m.proxies, list):
            logging.info("Variable 'proxies' is not a list")
            return False

    logging.debug("All tests have passed for %r" % m)
    return True


def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


def load_projects():
    """Loads projects from gconf directory"""

    projects = []
    for loader, modname, ispkg in pkgutil.iter_modules(gconf.__path__, gconf.__name__ + "."):
        if ispkg:
            logging.warning("Skipping %s because it's package" % modname)
            continue
        module = loader.find_module(modname).load_module(modname)

        if validate_module(module):
            projects.append(module)
        else:
            logging.warning("Module %r has failed testing" % module)
            continue

    if projects:
        return projects
    else:
        logging.error("Configs dir is empty or doesn't contain "
                      "valid config files")
        raise Exception


def getter(url, handle_content, handle_error, proxies, useragents):
    global timeout
    with gevent.Timeout(timeout):
        #time = random.randrange(1, 10)
        #print "Sleeping for %d seconds" % time
        #gevent.sleep(time)
        #proxy = urllib2.ProxyHandler(random.choice(proxies))
            try:
                data = urllib.urlencode(url.data)
                if url.post:
                    request = urllib2.Request(url.url, data)
                else:
                    request = urllib2.Request(url.url + "?" + data)
                request.add_header('User-agent', random.choice(useragents))
                index = urllib2.urlopen(request)
                handle_content(url, index.info().headers, index.read())
            except Exception as e:
                handle_error(url, e)


def main():
    global timeout
    print "gscraper %s" % __version__
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', dest='timeout', type=int, default=30, help="Timeout for fetcher (default: 30)")
    parser.add_argument('-w', dest='workers', type=int, default=50, help="Number of workers (default: 50)")
    args = parser.parse_args()
    timeout = args.timeout

    projects = load_projects()

    iprojects = [
        imap(lambda x: (x,
                        c.handle_content,
                        c.handle_error,
                        c.proxies,
                        c.useragents), c.urls) for c in projects]

    pool = Pool(args.workers)

    for n in roundrobin(*iprojects):
        pool.spawn(getter, *n)

    pool.join()

    for c in projects:
        c.handle_finish()

if __name__ == "__main__":
        main()
