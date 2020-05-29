"""
Url routing system for the site - in student_info app directory
"""

# imports path for url routing
from django.urls import path
# import views from the current directory
from . import views

# these urls are called when requested by the user on the main site
urlpatterns = [
    path('', views.home, name="home"),  # home page (linked to home function in views)
    path('report', views.report, name="pdf_view"),  # pdf report (linked to report function in views)
    path('help', views.help_page, name='help')  # help page (linked to help_page in views)
]
