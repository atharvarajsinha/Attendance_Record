import re
from pathlib import Path

from django.db import models


def scoped_student_image_path(instance: "Student", filename: str) -> str:
    return _scoped_media_path(
        "students",
        instance.school_code,
        instance.class_name,
        instance.section,
        filename,
    )


def scoped_attendance_image_path(instance: "AttendanceSession", filename: str) -> str:
    return _scoped_media_path(
        "attendance",
        instance.school_code,
        instance.class_name,
        instance.section,
        filename,
    )


def _scoped_media_path(
    prefix: str,
    school_code: str | None,
    class_name: str | None,
    section: str | None,
    filename: str,
) -> str:
    parts = [
        _safe_path_part(part)
        for part in [school_code, class_name, section]
        if part and part.strip()
    ]
    safe_filename = Path(filename).name
    return "/".join([prefix, *parts, safe_filename])


def _safe_path_part(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip()).strip("._-") or "unknown"


class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    school_code = models.CharField(max_length=100, blank=True)
    class_name = models.CharField(max_length=100, blank=True)
    section = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=scoped_student_image_path)
    embedding_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.student_id} - {self.full_name}"


class AttendanceSession(models.Model):
    school_code = models.CharField(max_length=100, blank=True)
    class_name = models.CharField(max_length=100, blank=True)
    section = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=scoped_attendance_image_path)
    detected_faces = models.PositiveIntegerField(default=0)
    ai_response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


class AttendanceRecord(models.Model):
    STATUS_CHOICES = (("Present", "Present"), ("Absent", "Absent"))
    session = models.ForeignKey(
        AttendanceSession, related_name="records", on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        Student, related_name="attendance_records", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session", "student")
