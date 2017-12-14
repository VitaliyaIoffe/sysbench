#!/usr/bin/python
import os
import sys
from urllib import urlencode
import requests

def parse_bench(filename):
    fileHandle = open(filename)
    lastline = fileHandle.readlines()
    fileHandle.close()
    return lastline

def get_version(filename):
    fileHandle = open(filename)
    lastline = fileHandle.readlines()[-1]
    fileHandle.close()
    return lastline.split()[0]

def push_to_microb(server, token, name, value, version, unit='trps', tab='sysbench'):
    uri = 'http://%s/push?%s' % (server, urlencode(dict(
        key=token, name=name, param=value,
        v=version, unit=unit, tab=tab
    )))

    r = requests.get(uri)
    if r.status_code == 200:
        print 'Export complete'
    else:
        print 'Export error http: %d' % r.status_code

def main():
    if len(sys.argv) < 3:
        print('Usage:\n./main.py [benchmarks-results.file] [tarantool-version.file]')
        exit(-1)

    values = parse_bench(sys.argv[1])
    version = get_version(sys.argv[2])

    # push bench data to microb-server
    if "MICROB_WEB_TOKEN" in os.environ and \
        "MICROB_WEB_HOST" in os.environ:
        for value in values:
            push_to_microb(
                os.environ['MICROB_WEB_HOST'],
                os.environ['MICROB_WEB_TOKEN'],
                value.split(":")[0],
                value.split(":")[1],
                version
            )
    else:
        print("MICROB params not specified")

    return 0

if __name__ == '__main__':
    main()