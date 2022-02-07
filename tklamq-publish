#!/usr/bin/python3
# Copyright (c) 2010-2021 Alon Swartz <alon@turnkeylinux.org> - all rights reserved
# Copyright (c) 2022 TurnKey GNU/Linux <admin@turnkeylinux.org> - all rights reserved

import os
import sys
import argparse
import json

from tklamq_lib.amqp import __doc__ as env_doc
from tklamq_lib.amqp import connect, encode_message


def fatal(s):
    print("error: " + str(s), file=sys.stderr)
    sys.exit(1)


def file_exists(path: str) -> str:
    #if path != '-' or not os.path.exists(path):
    if not os.path.exists(path):
        raise TypeError(f"File not found ({path})")
    return path


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="tklamq-publish",
        description="Publishes a message to exchange/routing_key",
        epilog=env_doc,
    )
    parser.add_argument(
        "exchange",
        help="name of exchange",
    )
    parser.add_argument(
        "routing_key",
        help="interpretation of routing key depends on exchange type",
    )
    parser.add_argument(
        "--input", "-i",
        type=file_exists,
        #help="content to send (path/to/file or '-' for stdin)",
        help="content to send (path/to/file)",
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="treat input as encoded json",
    )
    parser.add_argument(
        "--encrypt", "-e",
        action="store_true",
        help="encrypt message using secret TKLAMQ_SECRET",
    )
    parser.add_argument(
        "--sender", "-s",
        help="message sender",
    )
    parser.add_argument(
        "--non-persistent",
        dest="persistent",
        action="store_false",  # store persistance
        help="only store message in memory (not to disk)",
    )
    args = parser.parse_args()

    secret = None
    content = ''
    if args.encrypt:
        secret = os.getenv('TKLAMQ_SECRET', None)
        if not secret:
            fatal('TKLAMQ_SECRET not specified, cannot encrypt')

    if args.input:
        #if args.input == '-':
        with open(args.input) as fob:
            content = fob.read()

    if args.json:
        content = json.loads(content)

    message = encode_message(args.sender, content, secret=secret)

    conn = connect()
    conn.publish(args.exchange, args.routing_key,
                 message, persistent=args.persistent)


if __name__ == "__main__":
    main()
