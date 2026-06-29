from django.urls import path

from attendance.views import AttendanceVerifyView, StudentRegisterView

urlpatterns = [
    path("student/register/", StudentRegisterView.as_view(), name="student-register"),
    path("attendance/verify/", AttendanceVerifyView.as_view(), name="attendance-verify"),
]
