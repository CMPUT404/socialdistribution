from django.http import HttpResponse

def home(request):
    html = "<html><body>URL redirection is Working!</body></html>"
    return HttpResponse(html)
