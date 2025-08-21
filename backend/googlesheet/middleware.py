# middleware.py
class DisableCSPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Supprimer tous les headers CSP
        if 'Content-Security-Policy' in response:
            del response['Content-Security-Policy']
        if 'Content-Security-Policy-Report-Only' in response:
            del response['Content-Security-Policy-Report-Only']
        return response
