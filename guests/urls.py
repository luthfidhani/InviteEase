from django.urls import path
from . import views

app_name = "guests"

urlpatterns = [
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("", views.dashboard_view, name="dashboard"),
    path("desk/<int:desk_id>/", views.desk_view, name="desk"),
    path("screen/<int:screen_id>/", views.screen_view, name="screen"),
    path('desk/<int:desk_id>/walk-in/', views.walk_in_view, name='walk_in'),
    path('api/guests/search/', views.api_guest_search, name='api_guest_search'),
    path('guests/list/', views.guest_list_view, name='guest_list'),
]
