from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/<str:movie_id>/<str:movie_title>', views.add, name='add'),
    path('update/<int:post_id>/<str:redirect>', views.update, name='update'),
    path('delete/<int:post_id>/<str:redirect>', views.delete, name='delete'),
    path('posts/<str:movie_id>', views.posts, name='posts'),
    path('account', views.account, name='account')

]

static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)