6proxy4
=======

Proxy traffic from IPv6 to IPv4 back and forth.
Requires *useful* library (find it on my github page).

Unlike tinyproxy and other proxies:

1. Just mirrors traffic between sockets.
1. Has only neccessary settings
1. Only python is required to work
1. It was created by me :)

TODO:

1. Rework debug logging

Note that all addresses are resolved only once on start.


USAGE
-----


1. Install it by doing ./setup.py install
1. Create a config. An example config:
~~~python
$ cat /etc/pr64.py
#!/usr/bin/env python3

from proxy64 import *
from useful.resolver import r6

# KLIGA.RU
p = Proxy(src=Addr('127.0.0.1', 8081), dst=Addr(r6('kliga.ru'), 80))

p.start()
p.join()
~~~
1. Run it:
~~~
$ chmod +x /etc/pr64.py
$ ./pr64.py
  23:32:15 info 127.0.0.1:8081 => 2a01:4f8:131:1025::6:80: listening on 127.0.0.1:8081
~~~
1. ...
1. Profit!
