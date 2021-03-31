import os


def create_nginx_config(app):
    location = '/etc/nginx/sites-enabled/{}.config'.format(app.name)
    if os.path.exists(location):
        os.remove(location)
    with open(location, 'w') as nginx_config_file:
        nginx_config_file.writelines([
            'upstream {}'.format(app.name),
            '{',
            '    server unix:/{}/app/run/uwsgi.sock;'.format(app.location),
            '}',
            'server {',
            '    listen 80;',
            '    server_name {};'.format(app.domain),
            '    charset utf-8;',
            '    client_max_body_size 128M;',
            '    location /static {',
            '        alias {}/app/staticfiles;'.format(app.location),
            '    }',
            '    location /media {',
            '        alias {}/app/media;'.format(app.location),
            '    }',
            '    location / {',
            '        include uwsgi_params;',
            '        uwsgi_pass api_bm_erp_dev;',
            '        uwsgi_read_timeout 300s;',
            '        uwsgi_send_timeout 300s;',
            '   }',
            'access_log {}/app/logs/nginx/access.log'.format(app.location),
            'error_log {}/app/logs/nginx/error.log'.format(app.location),
            '}',
        ])
    os.system('nginx -s reload')


def create_service_config(app):
    location = '/etc/systemd/system/{}.service'.format(app.name)
    if os.path.exists(location):
        os.remove(location)
    with open(location, 'w') as config:
        config.writelines([
            '[Unit]',
            f'Description=Automated deployemnt of {app.name}',
            'After=network.target',
            '',
            '[Service]',
            'User=ubuntu',
            'Group=ubuntu',
            f'WorkingDirectory={app.location}/app',
            f'Environment="PATH={app.location}/venv/bin"',
            f'ExecStart={app.location}/venv/bin/uwsgi --ini {app.location}/app/config/uwsgi.ini'
            'Restart=always',
            'KillSignal=SIGQUIT',
            'Type=notify',
            'NotifyAccess=all',
            '',
            '[Install]',
            'WantedBy=multi-user.target'
        ])
