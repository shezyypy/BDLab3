from django.shortcuts import render
from .models import Course, Student, StudentCourse, Flight, FlightPassenger
from django.db.models import Count, Avg, Min, Max, F
from django.db.models.functions import ExtractYear
import json


def index(request):
    courses = Course.objects.all()

    stats = {
        "students": Student.objects.count(),
        "courses": Course.objects.count(),
        "avg_grade": StudentCourse.objects.aggregate(avg=Avg("grade"))["avg"],
    }

    return render(request, "courses.html", {
        "courses": courses,
        "stats": stats
    })

def course_list(request):
    courses = Course.objects.all().order_by('course_name')
    return render(request,'courses.html', {'courses': courses})


def students_list(request):
    students = Student.objects.all().order_by("last_name")
    return render(request, "students.html", {"students": students})


def enrollments(request):
    enrollments = StudentCourse.objects.select_related("student", "course").all()
    return render(request, "enrollments.html", {"enrollments": enrollments})


def olap_courses(request):
    qs = StudentCourse.objects.select_related("course")

    data = list(qs.values(
        Курс=F("course__course_name")
    ).annotate(
        Количество=Count("id"),
        Среднее=Avg("grade"),
        Минимум=Min("grade"),
        Максимум=Max("grade"),
    ))

    labels = [row["Курс"] for row in data]
    values = [row["Количество"] for row in data]

    return render(request, "olap.html", {
        "data": data,
        "title": "Аналитика по курсам",
        "labels": json.dumps(labels),
        "values": json.dumps(values),
        "chart_type": "pie"
    })

def olap_by_course(request):
    qs = StudentCourse.objects.select_related("course")

    data = list(qs.values(
        Курс=F("course__course_name")
    ).annotate(
        Количество=Count("id"),
        Среднее=Avg("grade"),
        Минимум=Min("grade"),
        Максимум=Max("grade"),
    ))

    labels = [row["Курс"] for row in data]
    values = [float(row["Среднее"]) for row in data]

    return render(request, "olap.html", {
        "data": data,
        "title": "Аналитика по курсам",
        "labels": json.dumps(labels),
        "values": json.dumps(values),
        "chart_type": "pie"
    })

def olap_by_student(request):
    data = StudentCourse.objects.values(
        Студент=F("student__last_name")
    ).annotate(
        Количество=Count("id"),
        Среднее=Avg("grade"),
        Минимум=Min("grade"),
        Максимум=Max("grade")
    )

    return render(request, "olap.html", {
        "title": "Roll-up по студентам",
        "data": data
    })

def olap_by_year(request):
    data = list(StudentCourse.objects.annotate(
        Год=ExtractYear("student__enrollment_date")
    ).values("Год").annotate(
        Количество=Count("id"),
        Среднее=Avg("grade"),
        Минимум=Min("grade"),
        Максимум=Max("grade")
    ).order_by("Год"))

    labels = [str(row["Год"]) for row in data]
    values = [float(row["Среднее"]) for row in data]

    return render(request, "olap.html", {
        "title": "Roll-up по годам",
        "data": data,
        "labels": json.dumps(labels),
        "values": json.dumps(values),
        "chart_type": "line"
    })

def olap_slice_course(request):
    course_id = request.GET.get('course_id')

    data = []
    if course_id:
        data = StudentCourse.objects.filter(
            course_id=course_id
        ).select_related('student').values(
            'student__first_name',
            'student__last_name',
            'grade'
        )

    courses = Course.objects.all()

    return render(request, "olap_slice_course.html", {
        "data": data,
        "courses": courses
    })

def olap_slice_student(request):
    student_id = request.GET.get('student_id')

    data = []
    if student_id:
        data = StudentCourse.objects.filter(
            student_id=student_id
        ).select_related('course').values(
            'course__course_name',
            'grade',
            'enrollment_date'
        )

    students = Student.objects.all()

    return render(request, "olap_slice_student.html", {
        "data": data,
        "students": students
    })

def olap_cube(request):
    data = StudentCourse.objects.values(
        Курс=F("course__course_name"),
        Студент=F("student__last_name")
    ).annotate(
        Средняя_оценка=Avg("grade"),
        Количество=Count("id")
    ).order_by('course__course_name')

    return render(request, "olap.html", {
        "title": "Куб: Курс × Студент",
        "data": data
    })

def airport_flights(request):
    flights = Flight.objects.using('airport').all()

    return render(request, "airport_flights.html", {
        "flights": flights
    })

def airport_passengers(request):
    passengers = FlightPassenger.objects.using('airport').all()

    return render(request, "airport_passengers.html", {
        "passengers": passengers
    })

def airport_manifest(request):
    data = FlightPassenger.objects.using('airport').select_related('flight')

    return render(request, "airport_manifest.html", {
        "data": data
    })

def airport_olap_flights(request):
    data = FlightPassenger.objects.using("airport").values(
        Рейс=F("flight__flight_number")
    ).annotate(
        Количество=Count("last_name")
    )

    return render(request, "airport_olap.html", {
        "title": "Roll-up по рейсам",
        "data": data
    })

def airport_olap_passengers(request):
    data = FlightPassenger.objects.using("airport").values(
        Пассажир=F("last_name")
    ).annotate(
        Количество_рейсов=Count("flight")
    )

    return render(request, "airport_olap.html", {
        "title": "Roll-up по пассажирам",
        "data": data
    })

def airport_slice_flight(request):
    flight_id = request.GET.get('flight')

    data = []
    if flight_id:
        data = FlightPassenger.objects.using('airport').filter(
            flight_id=flight_id
        )

    flights = Flight.objects.using('airport').all()

    return render(request, "airport_slice_flight.html", {
        "data": data,
        "flights": flights
    })

def airport_slice_passenger(request):
    last_name = request.GET.get('last_name')

    data = []
    if last_name:
        data = FlightPassenger.objects.using('airport').filter(
            last_name=last_name
        ).select_related('flight')

    passengers = FlightPassenger.objects.using('airport').values('last_name').distinct()

    return render(request, "airport_slice_passenger.html", {
        "data": data,
        "passengers": passengers
    })

def airport_cube(request):
    data = FlightPassenger.objects.using("airport").values(
        Рейс=F("flight__flight_number"),
        Пассажир=F("last_name")
    ).annotate(
        Количество=Count("seat")
    )

    return render(request, "airport_olap.html", {
        "title": "Куб: Рейс × Пассажир",
        "data": data
    })


def dashboard(request):
    stats = {
        "students": Student.objects.count(),
        "courses": Course.objects.count(),
        "avg_grade": StudentCourse.objects.aggregate(avg=Avg("grade"))["avg"],
        "flights": Flight.objects.using("airport").count(),
        "passengers": FlightPassenger.objects.using("airport").count(),
    }

    return render(request, "dashboard.html", {"stats": stats})

def top_students(request):
    data = list(StudentCourse.objects.values(
        Студент=F("student__last_name")
    ).annotate(
        Средний_балл=Avg("grade")
    ).order_by("-Средний_балл")[:5])

    labels = [row["Студент"] for row in data]
    values = [float(row["Средний_балл"]) for row in data]

    return render(request, "olap.html", {
        "data": data,
        "title": "Топ студентов",
        "labels": json.dumps(labels),
        "values": json.dumps(values),
        "chart_type": "bar"
    })