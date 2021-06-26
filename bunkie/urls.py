from django.urls import path,include
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('filter/', room_filter, name='filter'),
    path('comments/', CommentList.as_view()),
    path('comments/<int:pk>/', CommentDetail.as_view()),
    path('account/', include('account.urls'))
]
urlpatterns = format_suffix_patterns(urlpatterns)