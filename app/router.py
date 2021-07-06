from django.conf.urls import url, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/login?$', LoginView.as_view(), name='login'),
    url(r'^auth/signup?$', SignupView.as_view(), name='signup'),
    url(r'^subjects/?$', SubjectListView.as_view(), name='subjectList'),
    url(r'^challenges/?$', ChallengeListView.as_view(), name='challengeList'),
    url(r'^challenge/?$', ChallengeView.as_view(), name='challengeSpecific'),
    url(r'^posts/?$', PostListView.as_view(), name='postList'),
    url(r'^post/(?P<id>[0-9]+)/?$', PostView.as_view(), name='postSpecific'),
    url(r'^post/(?P<id>[0-9]+)/like/?$', LikeView.as_view(), name='likePost'),
]
