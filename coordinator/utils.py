# utils.py
import os
from django.core.files.storage import FileSystemStorage
from college_sports_management import settings
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.lib import colors
from django.core.files.base import ContentFile
from django.conf import settings

def generate_certificate(event, student, certificate_type):
    buffer = io.BytesIO()
    # Set the canvas to A5 landscape by flipping the dimensions
    c = canvas.Canvas(buffer, pagesize=(A5[1], A5[0]))

    # Define paths for background image and logo
    background_image_path = f"{settings.MEDIA_ROOT}/certificates/background_image.png"  # Ensure this path is correct
    logo_image_path = f"{settings.MEDIA_ROOT}/certificates/logo.png"  # Ensure this path is correct
    
    # Draw the background image
    c.drawImage(background_image_path, 0, 0, width=A5[1], height=A5[0], mask='auto')  # Adjust size as needed

    # Add logo to the certificate
    c.drawImage(logo_image_path, 450, 350, width=100, height=100, mask='auto')  # Adjust position and size as needed

    # Set font styles
    c.setFont("Helvetica-Bold", 24)  # Using a built-in font for simplicity
    c.setFillColor(colors.darkblue)  # Set text color

    # Title of the certificate
    c.drawCentredString(A5[1] / 2, 600, "Certificate of Achievement")
    
    # Add subtitle
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)  # Reset text color
    c.drawCentredString(A5[1] / 2, 560, f"Type: {certificate_type.capitalize()}")

    # Event details
    c.setFont("Helvetica", 14)
    c.drawString(50, 500, f"Event: {event.title}")
    c.drawString(50, 470, f"Date: {event.date.strftime('%B %d, %Y')}")  # Format the date as needed

    # Student details
    c.drawString(50, 400, f"Student: {student.full_name}")
    
    # Add a decorative border
    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    c.rect(30, 30, A5[1] - 60, A5[0] - 60, stroke=1, fill=0)  # Adjust the border size and position

    # Additional note or message
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.grey)  # Change color for this message
    c.drawString(50, 350, "This certifies that the above-mentioned student has successfully completed the event.")
    
    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(colors.black)  # Reset text color
    c.drawString(50, 30, "Signed by: [Coordinator Name]")

    # Optional: Draw decorative elements like lines or shapes
    c.setStrokeColor(colors.lightgrey)
    c.setLineWidth(1)
    c.line(30, 730, A5[1] - 30, 730)  # Top line

    c.showPage()
    c.save()
    
    # Save PDF to Certificate model
    buffer.seek(0)
    return ContentFile(buffer.read(), f"{student.full_name}_{certificate_type}_certificate.pdf")




def save_certificate(file_name, content):
    fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'certificates'))
    filename = fs.save(file_name, content)  # Ensure content is a File-like object
    return filename