#!/usr/bin/env python3

from proxy64 import *

# KLIGA.RU
p = Proxy(src=Addr('127.0.0.1', 6666), dst=Addr(r6('kliga.ru'), 80))
p.start()
p.join()