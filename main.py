import os
import subprocess
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2._page import PageObject

def create_blank_page(width, height):
    return PageObject.create_blank_page(width=width, height=height)

def manual_duplex_print_and_cleanup(input_pdf_path):
    reader = PdfReader(input_pdf_path)
    total_pages = len(reader.pages)

    # Read size of the first page
    first_page = reader.pages[0]
    width = float(first_page.mediabox.width)
    height = float(first_page.mediabox.height)

    # Add blank page if necessary
    if total_pages % 2 != 0:
        print("The total number of pages is odd. Adding a blank page.")
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_page(create_blank_page(width, height))
        pdf_bytes = BytesIO()
        writer.write(pdf_bytes)
        pdf_bytes.seek(0)
        reader = PdfReader(pdf_bytes)
        total_pages += 1

    # Odd pages in reverse order
    writer_odd = PdfWriter()
    for i in range(total_pages-1, -1, -1):
        if i % 2 == 0:
            writer_odd.add_page(reader.pages[i])

    odd_pdf_bytes = BytesIO()
    writer_odd.write(odd_pdf_bytes)
    odd_pdf_bytes.seek(0)

    # Even pages in reverse order
    writer_even = PdfWriter()
    for i in range(total_pages-1, -1, -1):
        if i % 2 == 1:
            writer_even.add_page(reader.pages[i])

    even_pdf_bytes = BytesIO()
    writer_even.write(even_pdf_bytes)
    even_pdf_bytes.seek(0)

    # Print command (Mac uses lpr)
    print("Printing odd pages (front side).")
    subprocess.run(["lpr"], input=odd_pdf_bytes.read())

    input("Press Enter after preparing to flip the paper...")

    print("Printing even pages (back side).")
    subprocess.run(["lpr"], input=even_pdf_bytes.read())

    print("All tasks are completed!")

if __name__ == "__main__":
    input_path = input("Please enter the path of the PDF file to print: ").strip()
    input_path = input_path.strip("'")

    if not os.path.exists(input_path):
        print("The file does not exist.")
    else:
        manual_duplex_print_and_cleanup(input_path)
