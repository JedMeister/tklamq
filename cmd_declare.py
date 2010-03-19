#!/usr/bin/python
# Copyright (c) 2010 Alon Swartz <alon@turnkeylinux.org> - all rights reserved
"""
Arguments:

    exchange        name of exchange
    exchange_type   exchange type (direct, topic, fanout)
    binding         queue binding (used by routing_key)
    queue           queue to bind to exchange using binding
"""

import sys
from tklamq.amqp import __doc__ as env_doc
from tklamq.amqp import connect

def usage():
    syntax = "Syntax: %s <exchange> <exchange_type> <binding> <queue>" % sys.argv[0]
    print >> sys.stderr, syntax, __doc__, env_doc
    sys.exit(1)

def fatal(s):
    print >> sys.stderr, "error: " + str(s)
    sys.exit(1)

def main():
    if not len(sys.argv) == 5:
        usage()

    exchange, exchange_type, binding, queue = sys.argv[1:]
    if not exchange_type in ('direct', 'topic', 'fanout'):
        fatal("Invalid exchange type")

    conn = connect()
    conn.declare(exchange, exchange_type, binding, queue)


if __name__ == "__main__":
    main()

