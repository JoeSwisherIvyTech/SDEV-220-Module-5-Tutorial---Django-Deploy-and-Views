from django.urls import path
from . import views

# create a list of url patterns that ties urls to function calls
urlpatterns = [
    path('', views.post_list, name='post_list'),
]
