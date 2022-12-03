from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add', views.add, name='add'),
    path('update/<int:task_id>', views.update, name='update'),
    path('delete/<int:task_id>', views.delete, name='delete'),
    path('search', views.search, name='search'),

]

static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)