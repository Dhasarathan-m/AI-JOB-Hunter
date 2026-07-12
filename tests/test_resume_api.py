import json
import unittest
from unittest import mock

from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


class ResumeApiTests(unittest.TestCase):
    def test_upload_resume_rejects_unsupported_type(self):
        response = client.post(
            "/resume/upload",
            files={"file": ("resume.txt", b"hello", "text/plain")},
        )
        self.assertEqual(response.status_code, 415)

    @mock.patch("backend.services.resume_service.ResumeMatchService.upload_resume")
    def test_upload_resume_success(self, upload_resume):
        upload_resume.return_value = {"resume_id": 1, "filename": "resume.pdf", "parsed_data": {}, "created_at": "2026-01-01T00:00:00"}
        response = client.post(
            "/resume/upload",
            files={"file": ("resume.pdf", b"pdfdata", "application/pdf")},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["resume_id"], 1)

    @mock.patch("backend.services.resume_service.ResumeMatchService.match_resume")
    def test_match_resume_not_found(self, match_resume):
        match_resume.side_effect = ValueError("Resume not found")
        response = client.post("/resume/match", params={"resume_id": 999})
        self.assertEqual(response.status_code, 404)
