from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('filter/', room_filter, name='filter'),
    path('comments/', CommentList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)