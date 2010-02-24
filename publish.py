#!/usr/bin/python
"""
Arguments:

    exchange        name of exchange
    routing_key     interpretation of routing key depends on exchange type
"""

import sys
from amqp import __doc__ as env_doc
from amqp import connect

def usage():
    print >> sys.stderr, "Syntax: %s <exchange> <routing_key>" % sys.argv[0]
    print >> sys.stderr, "Message is stdin"
    print >> sys.stderr, __doc__, env_doc
    sys.exit(1)

def main():
    if not len(sys.argv) == 3:
        usage()

    exchange, routing_key = sys.argv[1:]
    message = sys.stdin.read()

    conn = connect()
    conn.publish(exchange, routing_key, message)

if __name__ == "__main__":
    main()

