"""Connects to the memcached server, setting and deleting one key"""
from pymemcache.client import base as membase
import os
import sys
import json
import time


def main():
    memcache_host = os.environ['MEMCACHED_HOST']
    memcache_port = os.environ['MEMCACHED_PORT']
    mc_client = membase.Client((memcache_host, memcache_port))

    print('Fetching key test_key:')
    val = mc_client.get('test_key')
    if val is not None:
        print(f'Got weird value! Expected null, got {val}')
        sys.exit(1)

    original = {'foo': 7}
    original_json = json.dumps(original)
    print(f'Setting key test_key to: {original_json} (2 second expire time)')
    mc_client.set('test_key', original_json, expire=2)

    print('Fetching key test_key:')
    val = mc_client.get('test_key')
    if val != original_json:
        print(f'Got weird value! Expected {original_json}, got {val}')
        sys.exit(1)

    print('Sleeping 2.2 seconds to allow expiration')
    time.sleep(2.2)

    print('Fetching key test_key:')
    val = mc_client.get('test_key')
    if val is not None:
        print(f'Got weird value! Expected null, got {val}')
        sys.exit(1)

    print('All tests passed')


if __name__ == '__main__':
    main()
