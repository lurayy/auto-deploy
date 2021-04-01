import os
from sh import git


def update_app(app):
    home = '/home/ubuntu'
    os.chdir(home)
    if not os.path.exists(f'{app.location}'):
        git(f'clone {app.repo}')
        # os.system(f'git clone {app.repo}')
    os.chdir(f'{app.location}')
    git(f'checkout {app.branch}')
    git(f'pull origin {app.branch}')
    # os.system(f'git checkout {app.branch}')
    # os.system(f'git pull origin {app.branch}')
    os.system(f'sudo service {app.name}-{app.branch} restart')


def create_app(app):
    home = '/home/ubuntu'
    os.chdir(home)
    if not os.path.exists(f'{home}/{app.name}'):
        os.mkdir(f'{home}/{app.name}')
    os.chdir(f'{home}/{app.name}')
    print(app.location)
    if not os.path.exists(f'{app.location}'):
        # os.system(f'git clone {app.repo} {app.branch}')
        git(f'clone {app.repo} {app.branch}')
    os.chdir(f'{app.location}')
    git(f'checkout {app.branch}')

    git(f'pull origin {app.branch}')
    # os.system(f'git checkout {app.branch}')
    # os.system(f'git pull origin {app.branch}')
    create_env(app)
    create_uwsgi(app)
    create_service_config(app)
    create_nginx_config(app)


def create_nginx_config(app):
    location = f'/etc/nginx/sites-enabled/{app.name}-{app.branch}.config'
    if os.path.exists(location):
        os.system(f'sudo rm {location}')
    temp = app.location+f'/app/config/{app.name}-{app.branch}.config'
    with open(temp, 'w') as nginx_config_file:
        nginx_config_file.writelines([
            f'upstream {app.name}-{app.branch}',
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
    os.system(f'sudo cp {temp} {location}')
    os.system('nginx -s reload')


def create_service_config(app):
    location = f'/etc/systemd/system/{app.name}-{app.branch}.service'
    temp = app.location+f'/app/config/{app.name}-{app.branch}.service'
    if os.path.exists(location):
        print('asdfasdf')
        os.system(f'sudo rm {location}')
    print('oie')
    with open(temp, 'w') as config:

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
    print('here')
    os.system(f'sudo cp {temp} {location}')
    print('hasdf')
    os.chdir('/etc/systemd/system/')
    os.system('systemctl daemon-reload')
    os.system(f'systemctl enable {app.name}-{app.branch}.service')


def create_env(app):
    os.chdir(app.location)
    # have to do it manually for now
    os.system('sudo -u ubuntu virtualenv -p python3 venv')
    # os.system('sudo -u ubuntu -s source venv/bin/activate')
    # os.system('sudo -u ubuntu pip3 install -r requirements.txt')
    # os.system('sudo -u ubuntu -s deactivate')


def create_uwsgi(app):
    location = app.location+'/app/config/uwsgi.ini'
    if os.path.exists(location):
        os.remove(location)
    with open(location, 'w') as config:
        config.writelines([
            '[uwsgi]',
            'uid = ubuntu',
            'gid = ubuntu',
            'project_name = app',
            f'base_dir = {app.location}/app',
            f'virtualenv = {app.location}/venv'
            'chdir = %(base_dir)',
            'module =  %(project_name).wsgi:application',
            'master = true',
            'processes = 4',
            'post-buffering = 204800',
            'thunder-lock = True',
            'uwsgi-socket = %(base_dir)/run/uwsgi.sock',
            'chmod-socket = 666',
            'socket-timeout = 300',
            'reload-mercy = 8',
            'reload-on-as = 512',
            'harakiri = 50',
            'max-requests = 5000',
            'vacuum = true',
            'disable-logging = True',
            'logto = %(base_dir)/logs/uwsgi/uwsgi.log',
            'log-maxsize = 20971520',
            'log-backupname = %(base_dir)/logs/uwsgi/old-uwsgi.log',
            'touch-reload = %(base_dir)/src/',
            'max-worker-lifetime = 300'
        ])
