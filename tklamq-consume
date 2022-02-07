#!/usr/bin/python3
# Copyright (c) 2010-2021 Alon Swartz <alon@turnkeylinux.org> - all rights reserved
# Copyright (c) 2022 TurnKey GNU/Linux <admin@turnkeylinux.org> - all rights reserved

import os
import sys
import argparse

from tklamq_lib.amqp import __doc__ as env_doc
from tklamq_lib.amqp import connect, decode_message


def fatal(s):
    print("error: " + str(s), file=sys.stderr)
    sys.exit(1)


def decrypt_callback(message_data, message):
    encrypted = message_data['encrypted']
    secret = os.getenv('TKLAMQ_SECRET', None)

    if encrypted and not secret:
        fatal('TKLAMQ_SECRET not specified, cannot decrypt cipher text')

    sender, content, timestamp = decode_message(message_data, secret)
    print(content)

    message.ack()


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="tklamq-consume",
        description="Consumes messages from a queue",
        epilog=(f"{env_doc}"
                "    TKLAMQ_SECRET"
                "       decryption key (required if encrypted)")
    )
    parser.add_argument(
        "queue",
        help="queue to consume messages from",
    )
    args = parser.parse_args()

    conn = connect()
    conn.consume(args.queue, callback=decrypt_callback)


if __name__ == "__main__":
    main()
