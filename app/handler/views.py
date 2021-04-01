import json
from django.http import JsonResponse
from handler.models import Application
from handler.utils import update_app, create_app


def ping_server(request):
    created = False
    try:
        data_json = json.loads(request.body.decode(encoding='UTF-8'))
        app, created = Application.objects.get_or_create(
            repo=data_json['repository'],
            branch=data_json['data']['branch'],
            domain=data_json['data']['domain']
        )
        if created:
            create_app(app)
        else:
            update_app(app)
        response_json = {'status': True}
    except Exception as exp:
        if created:
            app.delete()
        response_json = {'status': False, 
                         'error': f'{exp.__class__.__name__}: {exp}'}
    return JsonResponse(response_json)
