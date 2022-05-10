from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, 'shop/404.html', {'title': '404 Page Not Found'}, status=404)

def permission_denied_view(request, exception):
    return render(request, 'shop/403.html', {'title': '403 permission denaided'}, status=403)

def bad_request_view(request, exception):
    return render(request, 'shop/400.html', {'title': '400 Bad request'}, status=400)

def server_error_view(request):
    return render(request, 'shop/500.html', {'title': '500 Server Error'}, status=500)