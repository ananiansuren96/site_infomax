from django.urls import path
from .views import PostView, PostDetailView,  robots_txt


urlpatterns = [
    path('', PostView.as_view(), name='post_list'),
    path('post/<int:post_id>/', PostDetailView.as_view(), name='post_detail'),
    path("robots.txt", robots_txt, name="robots"),
]
