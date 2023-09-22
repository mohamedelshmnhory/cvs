from django.urls import path

from . import views

# /api/jobs/
urlpatterns = [
    path('', views.job_list_create_view, name='job-list'),
    # path('<int:pk>/update/', views.job_update_view, name='job-edit'),
    # path('<int:pk>/delete/', views.job_destroy_view),
    path('<int:pk>', views.job_detail_view, name='job')
]