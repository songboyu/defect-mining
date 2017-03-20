### Redis Options
REDIS_HOST = "192.168.0.103"
REDIS_PORT = 6379
REDIS_DB = 0

### Celery Options
CELERY_ROUTES = {
    "tasks.drill": "concolic",
    "tasks.fuzz": "fuzzer"
}

### Environment Options
# directory contain concolic-qemu versions, relative to the directoy node.py is invoked in
QEMU_DIR = None
# directory containing the binaries, used by the concolic node to find binaries
BINARY_DIR = "binarys"
# directory containing the pcap corpus
PCAP_DIR = "pcap"

### concolic options
# how long to drill before giving up in seconds
DRILL_TIMEOUT = 600

### Fuzzer options
# how often to check for crashes in seconds
CRASH_CHECK_INTERVAL = 5
# how long to fuzz before giving up in seconds
FUZZ_TIMEOUT = 300
# how long before we kill a dictionary creation process
DICTIONARY_TIMEOUT = 300
# how many fuzzers should be spun up when a fuzzing job is received
FUZZER_INSTANCES = 3
# where the fuzzer should place it's results on the filesystem
FUZZER_WORK_DIR = "output"

### Node Options
FUZZER_WORKERS = 1
concolic_WORKERS = 4

MEM_LIMIT = None
