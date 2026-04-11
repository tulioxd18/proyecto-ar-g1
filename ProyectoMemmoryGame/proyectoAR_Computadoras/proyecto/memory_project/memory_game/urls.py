from django.urls import path
from . import views

urlpatterns = [
    path("", views.select_level, name="select_level"),
    path("play/basico/", views.play_basic, name="play_basic"),
    path("play/medio/", views.play_medium, name="play_medium"),
    path("play/avanzado/", views.play_hard, name="play_hard"),
    path("save_result/", views.save_result, name="save_result"),
    path("perfil/", views.profile, name="profile"),
]
