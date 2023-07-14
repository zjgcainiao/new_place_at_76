wsgi_app = 'prolube76site.wsgi:application'
pythonpath = '../prolube76site'
# command = '/Users/stephenwang/my_venv/bin/gunicorn'
loglevel = 'debug'
# loglevel = 'info'
bind = '0.0.0.0:8081'
worker = 4
# work class
work_class = 'sync'
# Write access and error info to /var/log
accesslog = errorlog = '../gunicorn/gunicorn-logfile-dev.log'
# PID file so you can easily fetch process ID
pidfile = "../gunicorn/gunicorn-dev.pid"
# Restart workers when code changes (development only!)
reload = True
#set to "*" to disable checking of Front-end IPs; useful when you don't know in advance the ip address of front-end, but you still trust the environment
proxy_protocol = True
proxy_allow_ips = '*'
daemon = True
# use this feature to allow the terminal to display the fully resolved conf.py file.
print_config = False  # True
# print_config = True