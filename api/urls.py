from django.urls import path
from .import views

urlpatterns = [
    path("logout/",views.logout),
    path("login/",views.login),
    path("register/",views.register),
    path("people/<int:id>",views.mehods),
    path("people/",views.people)
]