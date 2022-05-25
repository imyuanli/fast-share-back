from django.urls import path, include

from app_dashboard import views

urlpatterns = [
    path('api/get_source_list/', views.get_source_list, name='get_source_list'),
    path('api/insert_source/', views.insert_source, name='insert_source'),
    path('api/get_single_source/', views.get_single_source, name='get_single_source'),
    # path('api/get_collection/', views.get_collection, name='get_collection'),
    path('api/get_is_published/', views.get_is_published, name='get_is_published'),
    path('api/update_published/', views.update_published, name='update_published'),
    path('api/delete_published/', views.delete_published, name='delete_published'),
    path('api/search_source/', views.search_source, name='search_source'),
    path('api/insert_comment/', views.insert_comment, name='insert_comment'),
    path('api/get_comment_list/', views.get_comment_list, name='get_comment_list'),
]
