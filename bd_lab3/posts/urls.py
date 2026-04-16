from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard),
    path('courses/', views.course_list),
    path("students/", views.students_list),
    path("enrollments/", views.enrollments),
    path("olap/course/", views.olap_by_course),
    path("olap/student/", views.olap_by_student),
    path("olap/year/", views.olap_by_year),
    path("olap/slice-course/", views.olap_slice_course),
    path("olap/slice-student/", views.olap_slice_student),
    path("olap/cube/", views.olap_cube),
    path("olap/top-students/", views.top_students),
    path("airport/flights/", views.airport_flights),
    path("airport/passengers/", views.airport_passengers),
    path("airport/manifest/", views.airport_manifest),
    path("airport/olap/flights/", views.airport_olap_flights),
    path("airport/olap/passengers/", views.airport_olap_passengers),
    path("airport/olap/slice-flight/", views.airport_slice_flight),
    path("airport/olap/slice-passenger/", views.airport_slice_passenger),
    path("airport/olap/cube/", views.airport_cube),
]