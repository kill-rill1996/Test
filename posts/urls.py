from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, CommentView, CommentMixinsView


urlpatterns = [
    path('comments/<int:pk>/', CommentMixinsView.as_view()),
    path('comments/create/', CommentView.as_view()),

    path('posts/<int:pk>/comments/', CommentView.as_view()),
    path('posts/', PostViewSet.as_view({'get': 'list'})),
    path('posts/create/', PostViewSet.as_view({'post': 'create'})),
    path('posts/<int:pk>/', PostViewSet.as_view({'get': 'retrieve'})),
    path('posts/update/<int:pk>/', PostViewSet.as_view({'put': 'update'})),
    path('posts/delete/<int:pk>/', PostViewSet.as_view({'delete': 'destroy'})),

]

