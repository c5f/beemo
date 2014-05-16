from django.contrib.auth import logout
from django.http import HttpResponseRedirect

def logout_page(request):
    """Logout
    """

    logout(request)
    return HttpResponseRedirect('/')
