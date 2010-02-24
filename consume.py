#!/usr/bin/python
"""
Arguments:

    queue       queue to consume messages from
"""
import sys
from amqp import __doc__ as env_doc
from amqp import connect

def usage():
    print >> sys.stderr, "Syntax: %s <queue>" % sys.argv[0]
    print >> sys.stderr, __doc__, env_doc
    sys.exit(1)

def main():
    if not len(sys.argv) == 2:
        usage()

    queue = sys.argv[1]
    
    conn = connect()
    conn.consume(queue)

if __name__ == "__main__":
    main()

