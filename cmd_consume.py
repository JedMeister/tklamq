#!/usr/bin/python
"""
Arguments:

    queue       queue to consume messages from

If message content is encrypted, TKLAMQ_SECRET will be used as decryption key
"""

import os
import sys

from tklamq.amqp import __doc__ as env_doc
from tklamq.amqp import connect, decode_message

def usage():
    print >> sys.stderr, "Syntax: %s <queue>" % sys.argv[0]
    print >> sys.stderr, __doc__, env_doc
    sys.exit(1)

def fatal(s):
    print >> sys.stderr, "error: " + str(s)
    sys.exit(1)

def decrypt_callback(message_data, message):
    encrypted = message_data['encrypted']
    secret = os.getenv('TKLAMQ_SECRET', None)

    if encrypted and not secret:
        fatal('TKLAMQ_SECRET not specified, cannot decrypt cipher text')

    sender, content, timestamp = decode_message(message_data, secret)
    print content

    message.ack()

def main():
    if not len(sys.argv) == 2:
        usage()

    queue = sys.argv[1]
    
    conn = connect()
    conn.consume(queue, callback=decrypt_callback)

if __name__ == "__main__":
    main()

