# Importing required libraries
from django.urls import path
from lmsapp import views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),    
    path("", views.home, name="home"),  # Moved to the top
    path("issue/", views.issue, name="issue"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout"),
    path("return_item/", views.return_item, name="return_item"),
    path("history/", views.history, name="history"),
]
