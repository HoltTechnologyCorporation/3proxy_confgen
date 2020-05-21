#!/usr/bin/env python3
import json
from argparse import ArgumentParser
import sys
from pprint import pprint

import yaml


def load_servers(fname):
    with open(fname) as inp:
        return inp.read().splitlines()


def main():
    parser = ArgumentParser()
    parser.add_argument('action')
    parser.add_argument('upstreams')
    opts = parser.parse_args()

    upstream_reg = {}
    with open('var/config.yml') as inp:
        config = yaml.load(inp, Loader=yaml.Loader)
        for up in config['upstreams']:
            upstream_reg[up['name']] = up

    up_ids = opts.upstreams.split(',')
    for up_id in up_ids:
        if up_id not in upstream_reg:
            sys.stderr.write('Unknown action: %s' % up_id)
            sys.exit(1)

    if opts.action == '3proxy-conf':
        print(config['3proxy_config'])
        for up_id in up_ids:
            up = upstream_reg[up_id]
            listen_port = up['start_listen_port']
            config_mode = {
                    'socks': 'socks5',
                    'http': 'http',
                }[up['mode']]
            print('# %s' % up_id)
            for server in load_servers(up['proxy_file']):
                server_host, port = server.split(':')
                port = int(port)
                print('flush')
                print('auth iponly')
                print('allow * %s' % ','.join(config['whitelist_ips']))
                print('parent 1000 %s %s %d %s %s' % (
                    config_mode,
                    server_host, port,
                    up['username'],
                    up['password'],
                ))
                cmd = {
                        'socks': 'socks',
                        'http': 'proxy -a',
                    }[up['mode']]
                print('%s -p%d' % (cmd, listen_port))
                print('')
                listen_port += 1
    elif opts.action == 'proxy-list':
        for up_id in up_ids:
            up = upstream_reg[up_id]
            listen_port = up['start_listen_port']
            for server in load_servers(up['proxy_file']):
                print('%s:%d' % (
                    config['listen_ip'],
                    listen_port,
                ))
                listen_port += 1
            print('')


if __name__ == '__main__':
    main()
