from rest_framework import serializers

from attendance.models import (
    AttendanceRecord,
    AttendanceSession,
    AttendanceSessionImage,
    Student,
)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "student_id",
            "full_name",
            "email",
            "school_code",
            "class_name",
            "section",
            "image",
            "embedding_registered",
            "created_at",
        ]
        read_only_fields = ["embedding_registered", "created_at"]


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(source="student.student_id", read_only=True)
    full_name = serializers.CharField(source="student.full_name", read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ["student_id", "full_name", "status", "created_at"]


class AttendanceSessionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceSessionImage
        fields = ["id", "image", "created_at"]


class AttendanceSessionSerializer(serializers.ModelSerializer):
    records = AttendanceRecordSerializer(many=True, read_only=True)
    images = AttendanceSessionImageSerializer(many=True, read_only=True)

    class Meta:
        model = AttendanceSession
        fields = [
            "id",
            "school_code",
            "class_name",
            "section",
            "image",
            "images",
            "detected_faces",
            "records",
            "created_at",
        ]
