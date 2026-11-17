import time
from django.http import HttpResponse
from django.core.cache import cache



class RequestInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        ip = request.META.get("REMOTE_ADDR")

        print("_____________New Request__________________")
        print(f"Request Method: {request.method}")
        print(f"Request URL: {request.path}")
        print(f"IP Address: {ip}")

        response = self.get_response(request)

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Response Status Code: {response.status_code}")
        print(f"Execution Time: {execution_time:.4f} seconds")
        print("__________________________________________")
        return response

class RequestIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_ips = ["192.168.1.100", "192.168.1.101", "192.168.1.102"]

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")

        if ip in self.blocked_ips:
            print(f"[BLOCKED] Заблокована спроба доступу з IP: {ip}")
            return HttpResponse("Access Denied: Your IP is blocked.", status=403)

        response = self.get_response(request)
        return response

class TrackNumberValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        track_number = None
        if request.path.startswith('/parcels/'):
            parts = request.path.strip('/').split('/')
            if len(parts) > 1:
                track_number = parts[1]
        elif request.path.startswith('/search/'):
            track_number = request.GET.get('track')

        if track_number is not None:
            if not (10 <= len(track_number) <= 16 and track_number.startswith('UA')):
                print(f"[ERROR] Неправильний трек-номер: {track_number} (довжина: {len(track_number)})")
                return HttpResponse("Error: Invalid track number format! Must be 10-16 characters and start with UA.", status=400)

        response = self.get_response(request)
        return response

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        cache_key = f"rate_limit_{ip}"

        requests_count = cache.get(cache_key, 0)
        if requests_count >= 10:
            print(f"[RATE LIMIT] Перевищено ліміт запитів для IP: {ip}")
            return HttpResponse("Too Many Requests", status=403)

        if requests_count == 0:
            cache.set(cache_key, 1, 60)
        else:
            cache.incr(cache_key)

        response = self.get_response(request)
        return response