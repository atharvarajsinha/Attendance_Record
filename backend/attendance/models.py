from django.db import models


class Student(models.Model):
    student_id = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to="students/")
    embedding_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.student_id} - {self.full_name}"


class AttendanceSession(models.Model):
    image = models.ImageField(upload_to="attendance/%Y-%m-%d/")
    detected_faces = models.PositiveIntegerField(default=0)
    ai_response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)


class AttendanceRecord(models.Model):
    STATUS_CHOICES = (("Present", "Present"), ("Absent", "Absent"))
    session = models.ForeignKey(AttendanceSession, related_name="records", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name="attendance_records", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session", "student")
