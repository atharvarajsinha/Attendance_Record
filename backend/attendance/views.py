from django.db import transaction
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.ai_client import AIServiceClient, AIServiceError
from attendance.models import AttendanceRecord, AttendanceSession, Student
from attendance.serializers import AttendanceSessionSerializer, StudentSerializer


class StudentRegisterView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @transaction.atomic
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.save(embedding_registered=False)

        try:
            ai_response = AIServiceClient().register_face(student.student_id, student.image.path)
        except AIServiceError as exc:
            transaction.set_rollback(True)
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        student.embedding_registered = True
        student.save(update_fields=["embedding_registered"])
        return Response({"student": StudentSerializer(student).data, "ai": ai_response}, status=status.HTTP_201_CREATED)


class AttendanceVerifyView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @transaction.atomic
    def post(self, request):
        image = request.FILES.get("image")
        if image is None:
            return Response({"image": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        session = AttendanceSession.objects.create(image=image)
        try:
            ai_response = AIServiceClient().verify_attendance(session.image.path)
        except AIServiceError as exc:
            transaction.set_rollback(True)
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        session.detected_faces = int(ai_response.get("detected_faces", 0))
        session.ai_response = ai_response
        session.save(update_fields=["detected_faces", "ai_response"])

        statuses = {item["student_id"]: item["status"] for item in ai_response.get("students", [])}
        students = Student.objects.filter(student_id__in=statuses.keys())
        for student in students:
            AttendanceRecord.objects.create(session=session, student=student, status=statuses[student.student_id])
        print(session.ai_response)
        return Response(AttendanceSessionSerializer(session).data, status=status.HTTP_201_CREATED)
