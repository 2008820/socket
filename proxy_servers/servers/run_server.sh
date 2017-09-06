#!/usr/bin/env bash
nohup gunicorn --threads 100  --error-logfile ./error.log --access-logfile ./access.log -b 0.0.0.0:5111 servers:app &
#nohup gunicorn --threads 100  --error-logfile /home/xlzd/pyxd/proxy_servers/servers/error.log --access-logfile /home/xlzd/pyxd/proxy_servers/servers/access.log -b 0.0.0.0:5111 servers:app &
