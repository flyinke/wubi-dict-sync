from django.utils.deprecation import MiddlewareMixin

class NormalizeURLMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.path_info = request.path_info.replace('//', '/')
