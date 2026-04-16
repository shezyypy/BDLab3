from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.course_name


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    birth_date = models.DateField()
    enrollment_date = models.DateField()

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_column='student_id')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_column='course_id')
    grade = models.DecimalField(max_digits=3, decimal_places=2)
    enrollment_date = models.DateField()

    class Meta:
        db_table = 'student_courses'

    def __str__(self):
        return f"{self.student} - {self.course}"

class Flight(models.Model):
    flight_number = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=100)
    aircraft_number = models.CharField(max_length=50)

    class Meta:
        db_table = 'flights'

    def __str__(self):
        return f"Рейс {self.flight_number}"


class FlightPassenger(models.Model):
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        db_column='flight_number'
    )
    last_name = models.CharField(max_length=100, primary_key=True)
    seat = models.CharField(max_length=10)

    class Meta:
        db_table = 'flight_passengers'
        managed = False

    def __str__(self):
        return self.last_name