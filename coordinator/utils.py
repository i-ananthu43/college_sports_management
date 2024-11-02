# utils.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
import io

def generate_certificate(event, student, certificate_type):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.drawString(100, 750, f"Certificate of {certificate_type.capitalize()}")
    c.drawString(100, 700, f"Event: {event.title}")
    c.drawString(100, 650, f"Student: {student.full_name}")
    c.showPage()
    c.save()
    
    # Save PDF to Certificate model
    buffer.seek(0)
    return ContentFile(buffer.read(), f"{student.full_name}_{certificate_type}_certificate.pdf")
