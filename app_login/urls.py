from django.urls import path
from app_login import views


urlpatterns = [
    path('api/get_login/', views.get_login, name='get_login'),
    path('api/get_login_code/', views.get_login_code, name='get_login_code'),
    path('api/get_info/', views.get_info, name='get_info'),
    # path('api/update_info/', views.update_info, name='update_info'),
]
