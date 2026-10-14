from django.urls import path
from . import views


urlpatterns = [
    path('add_student/',views.add_student),
    path('add_marks/',views.add_marks),
    path('view_student/',views.view_student),
]