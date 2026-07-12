import unittest
from unittest import mock

from backend.utils.resume_parser import ResumeParser


class ResumeParserTests(unittest.IsolatedAsyncioTestCase):
    async def test_validate_upload_rejects_unsupported_type(self):
        parser = ResumeParser()
        fake_file = mock.Mock(filename="resume.txt", content_type="text/plain")
        fake_file.read = mock.AsyncMock(return_value=b"test")

        with self.assertRaises(Exception) as context:
            await parser.parse(fake_file)

        self.assertIn("Unsupported file type", str(context.exception))

    async def test_parse_docx_extracts_fields(self):
        parser = ResumeParser()
        docx_bytes = b"PK\x03\x04\x14\x00\x06\x00"
        fake_file = mock.Mock(filename="resume.docx", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        fake_file.read = mock.AsyncMock(return_value=docx_bytes)

        with mock.patch("backend.utils.resume_parser.Document") as fake_document:
            fake_document.return_value.paragraphs = [
                mock.Mock(text="Jane Doe"),
                mock.Mock(text="jane@example.com"),
                mock.Mock(text="Skills:"),
                mock.Mock(text="Python, SQL"),
            ]
            result = await parser.parse(fake_file)

        self.assertEqual(result["name"], "Jane Doe")
        self.assertEqual(result["email"], "jane@example.com")
        self.assertIn("Python", result["skills"])
        self.assertIn("SQL", result["skills"])
