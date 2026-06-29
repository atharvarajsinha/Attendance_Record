#!/usr/bin/env python
"""Register a student face directly inside the AI service.

This script does not start or call Django, React, or the FastAPI server. It loads
InsightFace Buffalo_L locally, extracts exactly one face embedding from the supplied
student image, and saves it as `student_<student_id>.npy` in the configured
embeddings directory.

Example:
    python register_student.py --student-id 101 --image ../media/students/student101.jpg
"""

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a student face embedding using only the AI service code.")
    parser.add_argument("--student-id", required=True, help="Student ID used in the embedding filename.")
    parser.add_argument("--image", required=True, help="Path to a student image containing exactly one face.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    image_path = Path(args.image)
    if not image_path.is_file():
        raise SystemExit(f"Image file not found: {image_path}")

    from app.face_engine import InsightFaceBuffaloEngine
    from app.recognition import register_student_face

    result = register_student_face(InsightFaceBuffaloEngine(), args.student_id, image_path.read_bytes())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
