"""
Admin site controls
"""
# imports admin from django
from django.contrib import admin

# imports Student data table from models.py
from .models import Student

# changes admin site header
admin.site.site_header = "Community Service Awards Program"


class StudentAdmin(admin.ModelAdmin):
    """StudentAdmin
    - sets the search fields, which columns to display on the table, and filter options
    """
    # can search for student name and number
    search_fields = ('name', 'number')
    # displays name, number, hours, grade, category, and date_created info on the table
    list_display = ('name', 'number', 'hours', 'grade', 'category', 'date_created')
    # can filter by grade or category
    list_filter = ('grade', 'category')


# registers the student data table and StudentAdmin class to the admin site
admin.site.register(Student, StudentAdmin)
