gscraper
========

gscraper is a tool to fetch urls for you using asynchronous sockets.

Description
-----------

The main idea that each project is a python script. It is just a fetcher,
and you have to provide callbacks to handle fetched content. The script fetches urls from all projects in chain one by one.
It can fetch urls using GET and POST requests.

Callbacks can be something which parses content or puts it to the db
or to some queue for further processing. Keep in mind that it **must not** be blocking or use much cpu time.

How to use
----------

Each module **must** have the next variables:

- urls - an iterable which yields Url instances.

Each module **should** have the next variables:

- handle_content callable,
- handle_error callable.

Also it **can** have variables:

- proxies - is a list of proxy servers,
- useragents - is a list of user agent strings.

Please, look into 'gconf' directory for examples.

How to generate urls
--------------------

_Urls_ variable is a list of urls. Each url is an instance of gconf.Url. This is a named tuple subclass.

    class Url(url, data=[], post=False, cookie=[])

There are variables:

- url is a string with url,
- data (optional) is a list of tuples (name, value),
- post (optional) is a True or False indicating method POST and GET accordingly,
- cookies (optional) is a list of tuples (name, value).
