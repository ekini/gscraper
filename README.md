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

