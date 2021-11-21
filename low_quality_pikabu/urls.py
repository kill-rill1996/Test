from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # path('posts/', include('posts.urls')),
    # path('', RedirectView.as_view(url='/posts')),

    # API
    path('api/', include('posts.urls'))

]
