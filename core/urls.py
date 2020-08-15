from django.urls import path
from rooms import views as room_views

app_name = "core"  # app name은 url.py의 namespace와 같아야 한다.

urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]

