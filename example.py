#!/usr/bin/env python3

from proxy64 import *
from useful.resolver import r4, r6

# KLIGA.RU
p = Proxy(src=Addr('127.0.0.1', 6666), dst=Addr(r6('kliga.ru'), 80))
p.start()
p.join()
