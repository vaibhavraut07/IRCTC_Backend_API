from django.http import JsonResponse
from django.conf import settings

class AdminAPIKeyMiddleware:
    """
    Middleware to check if the API key provided in the request headers matches the expected value.
    Only applied to admin routes.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only apply API key check to admin routes (e.g., /api/admin/)
        if request.path.startswith('/api/admin/'):
            api_key = request.headers.get('X-API-KEY')

            if api_key != settings.ADMIN_API_KEY:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

        return self.get_response(request)
