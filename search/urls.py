from django.conf.urls import url
from .views import search, detail

urlpatterns = [
    url('search', search),
    url('detail', detail)
]
