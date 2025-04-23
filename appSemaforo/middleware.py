from django.http import HttpResponseRedirect, HttpResponse
import threading

class CustomXFrameOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        thread_local = threading.local()

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        thread_local.request = request
        return self.get_response(request)

    def get_request():
        return getattr(thread_local, 'request', None)

class ProtectedErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except ProtectedError:
            template = get_template('protected_error.html')
            context = Context({'error': 'No se puede eliminar esta línea estratégica porque tiene dependencias con pilares sectoriales.'})
            return HttpResponse(template.render(context), status=500)