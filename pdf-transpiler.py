import csv
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO

# Path to font file
font_path = 'fonts/AlexBrush.ttf'
font_size = 16
font_name = 'AlexBrush'

# Register the custom font
pdfmetrics.registerFont(TTFont(font_name, font_path))

def add_name_to_pdf(input_pdf, output_pdf, name, y_position, color):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Set font and size
    c.setFont(font_name, font_size)
    c.setFillColorRGB(*color)

    # Get the width of the name text
    text_width = c.stringWidth(name, font_name, font_size)
    pdf_width = 360  # Width of the PDF page

    # Center the text horizontally
    x_position = (pdf_width - text_width) / 2

    # Draw the name on the canvas
    c.drawString(x_position, y_position, name)

    # Finalize the canvas and save it to the packet
    c.save()

    # Move to the beginning of the BytesIO buffer
    packet.seek(0)

    # Read the original PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Merge the new content with the existing PDF
    new_pdf = PdfReader(packet)
    page = reader.pages[0]
    page.merge_page(new_pdf.pages[0])

    # Add the modified page to the writer
    writer.add_page(page)

    # Write the output to a new PDF file
    with open(output_pdf, 'wb') as outputStream:
        writer.write(outputStream)

# Read CSV file and generate PDFs with personalized names
def generate_invites(event, guest_list, y_position, color):
    with open(guest_list, mode='r') as file:
        reader = csv.reader(file)

        for value in reader:
            name = value[0]
            output_dir = os.path.join("exports", event)
            os.makedirs(output_dir, exist_ok=True)

            output_pdf = os.path.join(output_dir, f"{name}.pdf")

            # Add the name to the PDF
            add_name_to_pdf(event + ".pdf", output_pdf, name, y_position, color)

wedding_color = (0.6784313725490196, 0.5137254901960784, 0.18823529411764706)
homecoming_color = (0.5568627450980392, 0.6, 0.6352941176470588)
generate_invites("wedding", "wedding_invitees.csv", 240, wedding_color)
generate_invites("homecoming", "homecoming_invitees.csv", 240, homecoming_color)