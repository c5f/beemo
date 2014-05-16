from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = patterns('',

    # Direct to our AngularJS index template at root.
    url(r'^$', login_required(TemplateView.as_view(template_name="index.html"))),
    
    # API URLs
    (r'^api/', include('api.urls')),
)
