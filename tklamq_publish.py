#!/usr/bin/python3
# Copyright (c) 2010-2021 Alon Swartz <alon@turnkeylinux.org> - all rights reserved
# Copyright (c) 2022 TurnKey GNU/Linux <admin@turnkeylinux.org> - all rights reserved
"""
Arguments:

    exchange            name of exchange
    routing_key         interpretation of routing key depends on exchange type

Options:

    -i --input=PATH     content to send (- for stdin)
    -j --json           treat input as encoded json
    -e --encrypt        encrypt message using secret TKLAMQ_SECRET
    -s --sender=        message sender
    --non-persistent    only store message in memory (not to disk)
"""

import os
import sys
import getopt
import simplejson as json

from tklamq.amqp import __doc__ as env_doc
from tklamq.amqp import connect, encode_message

def usage(e=None):
    if e:
        print("error: " + str(e), file=sys.stderr)

    print("Syntax: %s [-opts] <exchange> <routing_key>" % sys.argv[0], file=sys.stderr)
    print("Message is stdin", file=sys.stderr)
    print(__doc__, env_doc, file=sys.stderr)
    sys.exit(1)

def fatal(s):
    print("error: " + str(s), file=sys.stderr)
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'i:s:e:jh', 
           ['input=', 'sender=', 'encrypt', 'json', 'non-persistent'])

    except getopt.GetoptError as e:
        usage(e)

    inputfile = None
    sender = None
    opt_json = False
    opt_encrypt = False
    opt_persistent = True
    for opt, val in opts:
        if opt == '-h':
            usage()

        if opt in ('-i', '--input'):
            inputfile = val

        if opt in ('-s', '--sender'):
            sender = val

        if opt in ('-e', '--encrypt'):
            opt_encrypt = True

        if opt in ('-j', '--json'):
            opt_json = True

        if opt == "--non-persistent":
            opt_persistent = False

    if not len(args) == 2:
        usage()

    secret = os.getenv('TKLAMQ_SECRET', None)
    if opt_encrypt and not secret:
        fatal('TKLAMQ_SECRET not specified, cannot encrypt')

    # unset secret if encryption was not specified
    if not opt_encrypt:
        secret = None

    content = ''
    if inputfile == '-':
        content = sys.stdin.read()
    elif inputfile:
        content = file(inputfile).read()

    if opt_json:
        content = json.loads(content)

    exchange, routing_key = args
    message = encode_message(sender, content, secret=secret)

    conn = connect()
    conn.publish(exchange, routing_key, message, persistent=opt_persistent)

if __name__ == "__main__":
    main()

