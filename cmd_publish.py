#!/usr/bin/python
"""
Arguments:

    exchange            name of exchange
    routing_key         interpretation of routing key depends on exchange type

Options:

    -i --input=PATH     content to send (- for stdin)
    -e --encrypt        encrypt message using secret TKLAMQ_SECRET
"""

import os
import sys
import getopt

from amqp import __doc__ as env_doc
from amqp import connect, encode_message

def usage(e=None):
    if e:
        print >> sys.stderr, "error: " + str(e)

    print >> sys.stderr, "Syntax: %s [-opts] <exchange> <routing_key>" % sys.argv[0]
    print >> sys.stderr, "Message is stdin"
    print >> sys.stderr, __doc__, env_doc
    sys.exit(1)

def fatal(s):
    print >> sys.stderr, "error: " + str(s)
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'i:eh', ['input='])
    except getopt.GetoptError, e:
        usage(e)

    opt_input = None
    opt_encrypt = False
    for opt, val in opts:
        if opt == '-h':
            usage()

        if opt in ('-i', '--input'):
            opt_input = val

        if opt in ('-e', '--encrypt'):
            opt_encrypt = True

    if not len(args) == 2:
        usage()

    secret = os.getenv('TKLAMQ_SECRET', None)
    if opt_encrypt and not secret:
        fatal('TKLAMQ_SECRET not specified, cannot encrypt')

    # unset secret if encryption was not specified
    if not opt_encrypt:
        secret = None

    content = ''
    if opt_input == '-':
        content = sys.stdin.read()
    elif opt_input:
        content = file(opt_input).read()

    exchange, routing_key = args
    message = encode_message(content, secret=secret)

    conn = connect()
    conn.publish(exchange, routing_key, message)

if __name__ == "__main__":
    main()

