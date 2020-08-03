from django.urls import path, re_path
from app01.views import views,initial_ecs

urlpatterns = [
    re_path(r'^login/$', views.login, name="login"),
    re_path(r'^logout/$', views.logout, name='logout'),
    re_path(r'^index/$', views.index, name="index"),

    re_path(r'^initial-ecs/$', initial_ecs.initial, name='initial')


]