"""
Url routing system for the site
"""

# imports admin from django
from django.contrib import admin
# imports path and include for url routing
from django.urls import path, include

# these urls are called when requested by the user on the main site
urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),  # admindocs
    path('admin/', admin.site.urls, name="admin"),  # url path to admin page
    path('', include('student_info.urls'))  # includes the url paths in student_info/urls.py
]
