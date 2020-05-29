"""
Creates the filter used on the site
"""

# import django_filters module
import django_filters
# import Student model from models
from .models import Student


class StudentFilter(django_filters.FilterSet):
    """StudentFilter Class
    - creates a filter based on the Student model
    """
    class Meta:
        # sets the model to Student
        model = Student
        # allow user to filter by name, number, grade, and category
        fields = ['name', 'number', 'grade', 'category']
