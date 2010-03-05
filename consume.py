#!/usr/bin/python
"""
Arguments:

    queue       queue to consume messages from

if message['ciphertext'], TKLAMQ_SECRET will be used as decryption key
"""

import os
import sys

import tempfile
import shutil

import executil

from crypto import decrypt
from amqp import __doc__ as env_doc
from amqp import connect

def usage():
    print >> sys.stderr, "Syntax: %s <queue>" % sys.argv[0]
    print >> sys.stderr, __doc__, env_doc
    sys.exit(1)

def fatal(s):
    print >> sys.stderr, "error: " + str(s)
    sys.exit(1)

class TempFile(file):
    def __init__(self, prefix='tmp', suffix=''):
        fd, path = tempfile.mkstemp(suffix, prefix)
        os.close(fd)
        self.path = path
        self.pid = os.getpid()
        file.__init__(self, path, "w")

    def __del__(self):
        if self.pid == os.getpid():
            os.remove(self.path)

def execute(s):
    if s.startswith("#!"):
        fh = TempFile(prefix="tklamq-")
        fh.writelines(s)
        fh.close()

        try:
            os.chmod(fh.path, 0750)
            output = executil.getoutput(fh.path)
            print "successful: message processed (%s)" % fh.path
        except executil.ExecError, e:
            #todo: send 's' and 'e' back to hub
            print "failed to process message, sending error to hub..."

        return True
    return False

def decrypt_execute_callback(message_data, message):
    if type(message_data) == dict and message_data.has_key('ciphertext'):
        secret = os.getenv('TKLAMQ_SECRET', None)
        if not secret:
            fatal('TKLAMQ_SECRET not specified, cannot decrypt ciphertext')

        plaintext = decrypt(str(message_data['ciphertext']), secret)
    else:
        plaintext = str(message_data)

    if not execute(plaintext):
        print plaintext

    message.ack()

def main():
    if not len(sys.argv) == 2:
        usage()

    queue = sys.argv[1]
    
    conn = connect()
    conn.consume(queue, callback=decrypt_execute_callback)

if __name__ == "__main__":
    main()

