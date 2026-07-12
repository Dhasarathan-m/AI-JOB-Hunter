from __future__ import annotations

import re
from collections import defaultdict
from io import BytesIO
from typing import Any

import fitz
import pdfplumber
from docx import Document
from fastapi import HTTPException, UploadFile

from backend.config import settings

_ALLOWED_EXTENSIONS = {".pdf", ".docx"}
_ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


class ResumeParser:
    """Parse uploaded resumes into structured resume data."""

    def __init__(self) -> None:
        self.max_file_size = settings.resume_upload_max_size

    async def parse(self, resume_file: UploadFile) -> dict[str, Any]:
        raw_bytes = await resume_file.read()
        self._validate_upload(resume_file, raw_bytes)

        text = self._extract_text(raw_bytes, resume_file.filename)
        if not text.strip():
            raise HTTPException(status_code=422, detail="Unable to extract text from resume")

        parsed = self._parse_text(text)
        parsed["raw_text"] = text
        return parsed

    def _validate_upload(self, resume_file: UploadFile, raw_bytes: bytes) -> None:
        if resume_file.content_type not in _ALLOWED_CONTENT_TYPES:
            raise HTTPException(status_code=415, detail="Unsupported file type")

        extension = self._file_extension(resume_file.filename)
        if extension not in _ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=415, detail="Unsupported file type")

        if len(raw_bytes) > self.max_file_size:
            raise HTTPException(status_code=413, detail="Resume file is too large")

    @staticmethod
    def _file_extension(filename: str) -> str:
        return f".{filename.rsplit('.', 1)[-1].lower()}" if '.' in filename else ""

    def _extract_text(self, raw_bytes: bytes, filename: str) -> str:
        extension = self._file_extension(filename)
        if extension == ".pdf":
            return self._extract_pdf_text(raw_bytes)
        if extension == ".docx":
            return self._extract_docx_text(raw_bytes)
        raise HTTPException(status_code=415, detail="Unsupported resume format")

    def _extract_pdf_text(self, raw_bytes: bytes) -> str:
        text = self._extract_pdfplumber_text(raw_bytes)
        if text.strip():
            return text
        return self._extract_pymupdf_text(raw_bytes)

    def _extract_pdfplumber_text(self, raw_bytes: bytes) -> str:
        with pdfplumber.open(BytesIO(raw_bytes)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        return "\n".join(pages)

    def _extract_pymupdf_text(self, raw_bytes: bytes) -> str:
        document = fitz.open(stream=raw_bytes, filetype="pdf")
        pages = [page.get_text() for page in document]
        return "\n".join(pages)

    def _extract_docx_text(self, raw_bytes: bytes) -> str:
        document = Document(BytesIO(raw_bytes))
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        return "\n".join(paragraphs)

    def _parse_text(self, text: str) -> dict[str, Any]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        sections = self._split_sections(lines)

        skills = self._parse_list_section(sections.get("skills", []))
        education = self._parse_list_section(sections.get("education", []))
        certifications = self._parse_list_section(sections.get("certifications", []))
        projects = self._parse_list_section(sections.get("projects", []))
        experience = self._parse_list_section(sections.get("experience", []))

        return {
            "name": self._extract_name(lines),
            "email": self._extract_email(text),
            "phone": self._extract_phone(text),
            "skills": skills,
            "education": education,
            "certifications": certifications,
            "projects": projects,
            "experience": experience,
        }

    def _split_sections(self, lines: list[str]) -> dict[str, list[str]]:
        section_names = {
            "skills": ["skills", "technical skills", "skillset"],
            "education": ["education", "academic background", "education and training"],
            "certifications": ["certifications", "certificates", "licenses"],
            "projects": ["projects", "selected projects", "professional projects"],
            "experience": ["experience", "work experience", "professional experience"],
        }

        sections: dict[str, list[str]] = defaultdict(list)
        current_section = "summary"

        for line in lines:
            normalized = line.lower().rstrip(":")
            matched = False
            for section, names in section_names.items():
                if normalized in names:
                    current_section = section
                    matched = True
                    break
                if ":" in line:
                    prefix, value = line.split(":", 1)
                    if prefix.strip().lower() in names:
                        sections[section].append(value.strip())
                        matched = True
                        break
            if matched:
                continue
            sections[current_section].append(line)

        return sections

    def _parse_list_section(self, lines: list[str]) -> list[str]:
        if not lines:
            return []

        joined = "\n".join(lines)
        if "," in joined:
            items = [item.strip() for item in re.split(r"[,;\n]", joined) if item.strip()]
            return sorted(set(items), key=str.casefold)

        return [line for line in lines if line]

    def _extract_email(self, text: str) -> str | None:
        match = re.search(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", text)
        return match.group(0) if match else None

    def _extract_phone(self, text: str) -> str | None:
        match = re.search(r"\+?[0-9]{1,3}[\s\-]?(?:\(?[0-9]{2,4}\)?[\s\-]?)?[0-9\s\-]{5,15}", text)
        if not match:
            return None
        phone = match.group(0)
        return re.sub(r"\s+", " ", phone).strip()

    def _extract_name(self, lines: list[str]) -> str | None:
        for line in lines[:6]:
            if not line:
                continue
            if self._extract_email(line) or self._extract_phone(line):
                continue
            if re.search(r"(resume|curriculum vitae|cv)", line, re.I):
                continue
            if len(line.split()) > 6:
                continue
            return line
        return None
