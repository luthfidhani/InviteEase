from django.urls import path
from . import views

app_name = "guests"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("desk/<int:desk_id>/", views.desk_view, name="desk"),
    path("screen/<int:screen_id>/", views.screen_view, name="screen"),
]
