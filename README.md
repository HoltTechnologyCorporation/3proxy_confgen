# What is this?

Config generator for 3proxy server.
Config sets up 3proxy to use upstream proxy servers, for each upstream proxy server the separate port is provided on middle-server.


## How to use

Update "var/config.yml" with your settings. See Config File section.
Run `python3 build_config.py 3proxy <upstream-id>`. You can specify  multiple upstreams delimited by comma.
To generate list of ports on middle-server use command `python3 build_config.py proxy-server <upstream-id>`.


## Config File

```yaml
---
# This is IPs of servers allowed to use middle-server
whitelist_ips:
  - 127.0.0.1
  - 1.2.3.4
# This is IP of middle-server
listen_ip: 4.5.6.7
3proxy_config: |
  nserver 8.8.8.8
  nserver 1.1.1.1
  nscache 65536

upstreams:
  - name: super_cool_id
    username: username-for-upstream-proxy-auth
    password: password-for-upstream-proxy-auth
    # this port will be assigned to first upstream server,
    # then port + 1 will be assigned to second upstream server, and so on
    start_listen_port: 10000
    # "socks" or "http"
    mode: socks
    # upstream servers file
    proxy_file: var/some_file.txt
```
