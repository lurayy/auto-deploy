# import os
import requests
import json

# class dotdict(dict):
#     """dot.notation access to dictionary attributes"""
#     __getattr__ = dict.get
#     __setattr__ = dict.__setitem__
#     __delattr__ = dict.__delitem__


# def build_image(app):
#     home = '/home/ubuntu'
#     os.chdir(home)
#     if not os.path.exists(f'{home}/{app.repo}/'):
#         os.system(f'git clone {app.repo}')
#     os.chdir(f'{home}/{app.name}')
#     os.system(f'git checkout {app.branch}')
#     os.system(f'git pull origin {app.branch}')
#     os.system(f'sudo service {app.name}-{app.branch} restart')


# if __name__ == "__main__":
#     print('building image . . .')
#     app = {
#         'repo': 'git@github.com:ubuntu/mandalamayae-backend.git',
#         'name': 'mandalamayae-backend',
#         'branch': 'master'
#     }
#     build_image(dotdict(app))
data = {
    'repository': 'git@github.com:mandalaitsolutions/erp-booksmandala-backend.git',
    'data': {
        'branch': 'master',
        'domain': 'api.bm.erp.bizmandala.com'
    }
}
x = requests.post('http://40.121.7.188/', data=json.dumps(data))
print(x.text)
