from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from scan.models import Scanner, Scan, ApiKey

def scan(request, api_key_guid, scanner_name, target):
    api_key = get_object_or_404(ApiKey, guid = api_key_guid)
    if not api_key.active: return HttpResponse('<html><body><h1>401 Unauthorized</h1></body></html>', content_type = 'text/html', status = 401, reason = 'Unauthorized')
    scanner = get_object_or_404(Scanner, name = scanner_name)
    scanner.scan(target, api_key)

def bounce(request):
    return 
