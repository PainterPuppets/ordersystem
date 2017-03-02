from django.conf.urls import url
from orderApp.views import login
urlpatterns = [
    url(r'^login/$', login),
]
