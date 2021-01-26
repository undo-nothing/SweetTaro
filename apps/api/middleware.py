from django.utils.deprecation import MiddlewareMixin


class CsrfMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        if request.get_full_path().startswith('/v1.0/'):
            response['Access-Control-Allow-Origin'] = "*"
            response['Access-Control-Allow-Methods'] = "POST,OPTIONS,GET,DELETE,PUT,PATCH"
            response['Access-Control-Allow-Headers'] = "Content-Type, Authorization"
            response['Access-Control-Expose-Headers'] = "Content-Disposition"

            if request.method == "OPTIONS" and response.status_code == 401:
                # axios跨域复杂请求options时无法携带token
                response.status_code = 200

        return response
