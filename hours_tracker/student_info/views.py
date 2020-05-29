"""
Views - takes web requests and returns web responses
"""

# import render from django
from django.shortcuts import render
# import Student and History datatables from models.py
from .models import Student, History
# import StudentFilter from filters.py
from .filters import StudentFilter
# import modules for creating the pdf report
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# import datetime for formatting the date for the monthly report
import datetime


def calc_totals(students):
    """Calculate totals
    - calculates total students in each category
    - calculates total chapter hours
    :param students: inputted student data
    :return: list of total students per category and total chapter hours
    """

    # set initial values to 0
    total_bronze = 0
    total_silver = 0
    total_gold = 0
    total_chap_hours = 0

    # loop through each student in the inputted students data to calculate the totals
    for student in students:
        # if student is a dictionary (like in the report function)
        if type(student) == dict:
            if student['category'] == 'Bronze':
                total_bronze += 1
            elif student['category'] == 'Silver':
                total_silver += 1
            elif student['category'] == 'Gold':
                total_gold += 1

            # add all student hours together for total chapter hours
            total_chap_hours += int(student['hours'])
        # if student is a queryset (like in the home function)
        else:
            if student.category == 'Bronze':
                total_bronze += 1
            elif student.category == 'Silver':
                total_silver += 1
            elif student.category == 'Gold':
                total_gold += 1

            # add all student hours together for total chapter hours
            total_chap_hours += int(student.hours)

    # add the totals to a dictionary
    totals = [total_chap_hours, total_bronze, total_silver, total_gold]

    # return totals dictionary
    return totals


def home(request):
    """Home page function
    - passes the student info data from the database into the home.html file
    :param request: web requests
    :return: render (pass data to home.html)
    """
    # instantiate students object with all student data
    students = Student.objects.all()

    # calculate the totals with calc_totals from all of the student data
    totals = calc_totals(students)

    # retrieve the user input on the student filter
    student_filter = StudentFilter(request.GET, queryset=students)

    # create a dictionary with student info, total calculations, and student_filter
    student_info = {'students': students, 'total_chap_hours': totals[0], 'total_bronze': totals[1],
                    'total_silver': totals[2], 'total_gold': totals[3], 'student_filter': student_filter}

    # pass the data into home.html
    return render(request, 'student_info/home.html', student_info)


def render_to_pdf(template_src, context_dict={}):
    """Create the pdf
    :param template_src: html template for the pdf
    :param context_dict: dictionary data to render the pdf
    :return: http response object
    """
    # template for pdf
    template = get_template(template_src)
    # render the pdf
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    # if there are no errors, return http response object
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def report(request):
    """Report function
    - passes and retrieves data from report.html
    :param request: web requests
    :return: Http response object (view pdf)
    """
    # data selected by user
    selected_date = request.POST['selected_date']  # YYYY-MM
    # year selected by user from selected_date
    year = selected_date[:4]
    # month selected by user from selected_date
    month = selected_date[6:]

    # format the month to month name using datetime object (for pdf report)
    datetime_object = datetime.datetime.strptime(month, "%m")
    full_month_name = datetime_object.strftime("%B")

    # instantiating students and histories objects from the Student and History data tables
    students = Student.objects.all()
    histories = History.objects.all().order_by('date_modified')  # order the history records by the date_modified

    # create empty list for selected students
    selected_students = []

    # loop through each student in students
    for student in students:
        # filter out the students who were created/modified before or within the selected month
        student_histories = histories.filter(number=student.number, date_modified__year__lte=year,
                                             date_modified__month__lte=month)

        # if the student was created after the selected month then skip to the next student
        if student_histories.count() == 0:
            continue

        # find the most recently modified record of that student before or within the selected month
        last_record = student_histories[student_histories.count()-1]

        # set the award category for the student based on the last record's hours
        if 50 <= last_record.hours < 200:
            category = 'Bronze'
        elif 200 <= last_record.hours < 500:
            category = 'Silver'
        elif last_record.hours >= 500:
            category = 'Gold'
        else:
            category = 'N/A'

        # create a dictionary with the student's info including the modified hours for the selected month
        selected_student = {'name': student.name, 'number': student.number, 'grade': student.grade,
                            'hours': last_record.hours, 'category': category}

        # append each student's info to the selected_students list
        selected_students.append(selected_student)

    # calculate the totals for categories and chapter hours with the filtered student data
    totals = calc_totals(selected_students)

    # create a dictionary with the filtered student data
    student_info = {'students': selected_students, 'total_chap_hours': totals[0], 'total_bronze': totals[1],
                    'total_silver': totals[2], 'total_gold': totals[3], 'year': year, 'month': full_month_name}

    # create a pdf using the report.html template and filtered student data
    pdf = render_to_pdf('student_info/report.html', student_info)
    # return http response object to view the pdf
    return HttpResponse(pdf, content_type='application/pdf')


def help_page(request):
    """Help page
    :param request: web requests
    :return: render (help.html)
    """
    return render(request, 'student_info/help.html')
