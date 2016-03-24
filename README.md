1. 启动celery的命令行
$celery -A app.celery worker --loglevel=info

2.uwsgi配置样例
[uwsgi]
plugins = python
base = /opt/www/project1
pythonpath = %(base)
home = %(base)/env
module = run
app = app
callable = app
3.nginx配置样例

upstream uwsgi_flask {
  # server unix:/run/uwsgi/%(deb-confnamespace)/%(deb-confname)/socket;
}

location / {
     try_files $uri @flask;
     client_max_body_size 100m;
}

location @flask {
    uwsgi_pass uwsgi_flask;
    uwsgi_param X-Real-IP $remote_addr;
    uwsgi_param Host $http_host;
    include uwsgi_params;
}

4. bsd配置样例
#cat /etc/rc.conf
uwsgi_enable="YES"
uwsgi_flags=" -M -L -p 4 --vhost --no-site --uid 80 --gid 80 --max-fd 32768 --enable-threads  --emperor /usr/local/etc/uwsgi/vassals"

#cat vassals/my_app.ini
[uwsgi]
base = /usr/local/apps/my_app
pythonpath = %(base)/apps
home = %(base)/env
module = run
app = app
callable = app
chmod-socket = 644
socket = /tmp/my_app.sock
