from django.conf.urls import url, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
]
