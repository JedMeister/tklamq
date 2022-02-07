#!/usr/bin/python3
# Copyright (c) 2010-2021 Alon Swartz <alon@turnkeylinux.org> - all rights reserved
# Copyright (c) 2022 TurnKey GNU/Linux <admin@turnkeylinux.org> - all rights reserved

import sys
import argparse

from tklamq.amqp import __doc__ as env_doc
from tklamq.amqp import connect


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="tklamq-declare",
        description="Declares an exchange/binding/queue",
        epilog=env_doc,
    )
    parser.add_argument(
        "exchange",
        help="name of exchange",
    )
    parser.add_argument(
        "exchange-type",
        choices=['direct', 'topic', 'fanout'],
        help="exchange type (direct, topic, fanout)",
    )
    parser.add_argument(
        "binding",
        help="queue binding (used by routing_key)",
    )
    parser.add_argument(
        "queue",
        help="queue to bind to exchange using binding",
    )
    args = parser.parse_args()

    conn = connect()
    conn.declare(args.exchange, args.exchange_type, args.binding, args.queue)


if __name__ == "__main__":
    main()
