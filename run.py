#!/usr/bin/env python

import logging

import os
import sys
import redis
import tasks
import config as config

l = logging.getLogger("mining")
l.setLevel("INFO")

'''
Large scale test script. Should just require pointing it at a directory full of binaries.
'''
def start(binary_dir):

    jobs = [ ]
    binaries = os.listdir(binary_dir)
    for binary in binaries:
        if binary.startswith("."):
            continue 

        pathed_binary = os.path.join(binary_dir, binary)
        if os.path.isdir(pathed_binary):
            continue
        if not os.access(pathed_binary, os.X_OK):
            continue

        identifier = binary[:binary.rindex("_")]
        # remove IPC binaries from largescale testing
        if (identifier + "_02") not in binaries:
            jobs.append(binary)

    l.info("%d binaries found", len(jobs))
    l.debug("binaries: %r", jobs)

    # send all the binaries to the celery queue
    l.info("%d binaries found", len(jobs))

    filter_t = set()
    try:
        pwned = open("pwned").read()
        for pwn in pwned.split("\n")[:-1]:
            filter_t.add(pwn)
        l.info("already pwned %d", len(filter_t))
    except IOError:
        pass

    jobs = filter(lambda j: j not in filter_t, jobs)

    l.info("going to work on %d", len(jobs))

    for binary in jobs:
        tasks.fuzz.delay(binary)

    l.info("listening for crashes..")

    redis_inst = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
    p = redis_inst.pubsub()

    p.subscribe("crashes")

    cnt = 1
    for msg in p.listen():
        if msg['type'] == 'message':
            l.info("[%03d/%03d] crash found for '%s'", cnt, len(jobs), msg['data'])
            cnt += 1

def main(argv):
    binary_dir = config.BINARY_DIR
    start(binary_dir)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
