from django.shortcuts import redirect

def redirect_blog(request):
    return redirect('list',permanent=True)