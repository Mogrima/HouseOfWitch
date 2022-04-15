from django.shortcuts import render



def page_not_found_view(request, exception):
    return render(request, 'shop/404.html', status=404)

def permission_denied_view(request, exception):
    return render(request, 'shop/403.html', status=403)

def bad_request_view(request, exception):
    return render(request, 'shop/400.html', status=400)

def server_error_view(request):
    return render(request, 'shop/500.html', status=500)