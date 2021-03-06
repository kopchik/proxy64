#!/usr/bin/env python3

from collections import namedtuple
from useful.log import Log
import threading
import socket
import select
import syslog
import random
try:
  import ipaddress
except ImportError:
  try:
    import ipaddr as ipaddress
  except ImportError:
    raise Exception("you need ipaddr or ipaddress extensions")


Kb = 1024*1024
Mb = 1024*Kb
cnt = 0


Addr = namedtuple('Addr', ['ip', 'port'])
Addr.__str__  = lambda self: "%s:%s" % (self.ip, self.port)


class Tun(threading.Thread):
  def __init__(self, s, dst, buf, timeout=1):
    global cnt
    cnt += 1
    super().__init__()
    self.s1 = s
    self.dst = dst
    self.buf = buf
    self.timeout = timeout
    self.log = Log("{} {}".format(dst, cnt))

  def run(self):
    s1 = self.s1
    try:
      s2 = socket.create_connection(self.dst, self.timeout)
    except Exception as err:
      self.log.error(err)
      s1.close()
      return
    ss = [s1,s2]
    while True:
      #if __debug__: self.log.debug("waiting for events")
      rlist, _, xlist = select.select(ss, [], ss)
      if xlist:
        selg.log.info("connection problems on %s" % xlist)
        for s in ss: s.close()
        return

      for FROM in rlist:
        TO = s1 if FROM == s2 else s2
        data = FROM.recv(self.buf)
        #if __debug__: self.log.debug("got %s: %s" % (FROM.getpeername(), data))
        if not data:
          #if __debug__: self.log.debug("connection closed by {}, closing connection".format(FROM))
          for s in ss: s.close()
          return
        TO.sendall(data)


class Proxy(threading.Thread):
  def __init__(self, src=None, dst=None, buf=128*Kb, backlog=128):
    assert src and dst, \
      "please specify src and dst addresses"
    self.src = src
    self.dst = dst
    self.buf = buf
    self.backlog = backlog
    self.log = Log("%s => %s" % (src, dst))
    super().__init__()

  def run(self):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.log.info("listening on {}".format(self.src))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(self.src)
    s.listen(self.backlog)
    while True:
      #if __debug__: self.log.debug("waiting for incoming connections on {}"
      #  .format(self.src))
      conn, addr = s.accept()
      #if __debug__: self.log.debug("connection from {}".format(addr))
      tun = Tun(conn, self.dst, self.buf)
      tun.start()


if __name__ == '__main__':
  p = Proxy(src=Addr('127.0.0.1', 6666), dst=Addr('messir.net', 80))
  p.start()
  p.join()
