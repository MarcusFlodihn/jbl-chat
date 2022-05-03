from django.urls import path
from . import views

urlpatterns = [
    path("users/<int:user_id>/conversation", views.conversation),
    path("users/<int:user_id>/message", views.message),
    path("users", views.users)
]
