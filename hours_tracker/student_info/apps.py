"""
App settings
"""

# import AppConfig from django
from django.apps import AppConfig


class StudentInfoConfig(AppConfig):
    """Settings for student_info app,
    - includes the Configuration to be added to INSTALLED_APPS in settings.py
    """
    name = 'student_info'
