#!/usr/bin/env python

import logging
import os
import subprocess
import sys
import config

logging.info('Starting logger for...')
l = logging.getLogger("mining.node")
l.setLevel("DEBUG")

def check_exec(d, p):
    path = os.path.join(d, p)
    return not os.path.isdir(path) and os.access(path, os.X_OK)

def binary_dir_sane():
    if not os.path.isdir(config.BINARY_DIR):
        l.error("the binary directory specified in the config is not a directory")
        return False

    if not any(filter(lambda x: check_exec(config.BINARY_DIR, x), os.listdir(config.BINARY_DIR))):
        l.error("no binary files detected in binary directory specified")
        return False

    return True

def concolic_node(n, outfile, errfile):

    if not binary_dir_sane():
        return 1

    l.info("spinning up a concolic node with %d workers", n)
    args = ["celery", "-A", "tasks", "worker", "-c", str(n), "-Q", "concolic", "--loglevel=info", "-n", "concolic.%h"]

    with open(outfile, "w") as o:
        with open(errfile, "w") as e:
            subprocess.Popen(args, stdout=o, stderr=e)

def fuzzer_node(n, outfile, errfile):

    if not binary_dir_sane():
        return 1

    l.info("spinning up a fuzzer node with %d workers", n)

    args = ["celery", "-A", "tasks", "worker", "-c", str(n), "-Q", "fuzzer", "--loglevel=info", "-Ofair", "-n", "fuzzer.%h"]

    with open(outfile, "w") as o:
        with open(errfile, "w") as e:
            subprocess.Popen(args, stdout=o, stderr=e)

def main():
    if config.concolic_WORKERS:
        concolic_node(config.concolic_WORKERS, "log/concolic-out.log", "log/concolic-err.log")
    if config.FUZZER_WORKERS:
        fuzzer_node(config.FUZZER_WORKERS, "log/fuzzer-out.log", "log/fuzzer-err.log")

if __name__ == "__main__":
    sys.exit(main())
