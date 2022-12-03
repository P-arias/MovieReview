from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add/<str:movie_id>/<str:user_name>', views.add, name='add'),
    path('posts/<str:movie_id>', views.posts, name='posts'),

]

static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)