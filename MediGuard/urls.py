from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from .views import user_dashboard

app_name = 'MediGuard'
urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login/', views.login, name='login'),
    path('accounts/', include('allauth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('report/', views.report, name='report'),
    path('<int:report_id>/report_submitted/', views.report_submitted, name='report_submitted'),
    path('report_list/', views.report_list, name='report_list'),
    path('<int:report_id>/report_detail/', views.report_detail, name='report_detail'),
    path('report_list/', views.report_list, name='report_list'),
    path('delete_report/<int:pk>/', views.delete_report, name='delete_report'),
    path('<int:practice_id>/practice_detail/', views.practice_detail, name='practice_detail')
]
    # TODO: Add anonoymous access path
