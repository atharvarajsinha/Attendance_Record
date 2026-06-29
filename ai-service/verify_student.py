#!/usr/bin/env python
"""Verify attendance directly inside the AI service without Django or React.

Examples:
    python verify_student.py --image ../media/attendance/2026-06-29/classroom.jpg
    python verify_student.py --register --student-id 101 --image ../media/students/student101.jpg
"""

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Register or verify faces using only the AI service code.")
    parser.add_argument("--image", required=True, help="Path to a student or classroom image.")
    parser.add_argument(
        "--register",
        action="store_true",
        help="Register one student face instead of verifying attendance against existing embeddings.",
    )
    parser.add_argument("--student-id", help="Student ID required when --register is used.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image_path = Path(args.image)
    if not image_path.is_file():
        raise SystemExit(f"Image file not found: {image_path}")
    if args.register and not args.student_id:
        raise SystemExit("--student-id is required when --register is used")

    from app.face_engine import InsightFaceBuffaloEngine
    from app.recognition import register_student_face, verify_attendance_image

    face_engine = InsightFaceBuffaloEngine()
    image_bytes = image_path.read_bytes()

    if args.register:
        result = register_student_face(face_engine, args.student_id, image_bytes)
    else:
        result = verify_attendance_image(face_engine, image_bytes)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
