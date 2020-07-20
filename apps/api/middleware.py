from django.utils.deprecation import MiddlewareMixin


class CsrfMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if request.get_full_path().startswith('/v1.0/'):
            response['Access-Control-Allow-Origin'] = "*"
            response['Access-Control-Allow-Methods'] = "POST,OPTIONS,GET,DELETE,PUT,PATCH"
            response['Access-Control-Allow-Headers'] = "Content-Type"
        return response
