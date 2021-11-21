from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, CommentView


urlpatterns = [
    path('posts/', PostViewSet.as_view({'get': 'list'})),
    path('posts/create/', PostViewSet.as_view({'post': 'create'})),
    path('posts/<int:pk>/', PostViewSet.as_view({'get': 'retrieve'})),
    path('posts/<int:pk>/update', PostViewSet.as_view({'put': 'update'})),
    path('posts/<int:pk>/delete', PostViewSet.as_view({'delete': 'destroy'})),

    path('posts/comments/<int:pk>/', CommentView.as_view()),

]

