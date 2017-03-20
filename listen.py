#!/usr/bin/env python

import cPickle as pickle
import logging
import os
import sys

import redis

import config

'''
listen for new inputs produced by concolic

:param queue_dir: directory to places new inputs
:param channel: redis channel on which the new inputs will be arriving
'''

queue_dir = sys.argv[1]
channel   = sys.argv[2]

logging.info('Starting logger for...')
l = logging.getLogger("mining.listen")

l.debug("subscring to redis channel %s" % channel)
l.debug("new inputs will be placed into %s" % queue_dir)

try:
    os.makedirs(queue_dir)
except OSError:
    l.warning("could not create output directory '%s'" % queue_dir)

redis_inst = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
p = redis_inst.pubsub()

p.subscribe(channel)

input_cnt = 0 

for msg in p.listen():
    if msg['type'] == 'message':
        real_msg = pickle.loads(msg['data'])
        out_filename = "concolic-%d-%x-%x" % real_msg['meta']
        out_filename += "_%s" % real_msg['tag']
        l.debug("dumping new input to %s" % out_filename)
        afl_name = "id:%06d,src:%s" % (input_cnt, out_filename)
        out_file = os.path.join(queue_dir, afl_name)

        with open(out_file, 'wb') as ofp:
            ofp.write(real_msg['data'])

        input_cnt += 1

