from django.conf.urls import url, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^subjects/?$', SubjectListView.as_view(), name='subjectList'),
    url(r'^challenges/?$', ChallengeListView.as_view(), name='challengeList'),
    url(r'^auth/login?$', LoginView.as_view(), name='login'),
    url(r'^auth/signup?$', SignupView.as_view(), name='signup'),
]
