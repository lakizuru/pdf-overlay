import fitz  # PyMuPDF
from PIL import Image, ImageChops, ImageEnhance
import subprocess
import os
import pypdftk
import argparse

multiline_description = """Remove white background from a PDF and overlay it on another PDF.\n
Perfect for merging annotated or highlighted documents onto standardized templates."""

def remove_white_background(image_path):
    """
    Remove the white background from an image and return the image with transparency.
    """
    image = Image.open(image_path).convert("RGBA")
    r, g, b, a = image.split()

    # Create a mask using white color
    white_mask = Image.eval(image.convert("RGB"), lambda x: 255 if x < 255 else 0)
    white_mask = white_mask.convert("L")

    # Invert the mask
    transparent_mask = ImageChops.invert(white_mask)

    # Apply the mask to the alpha channel
    image.putalpha(transparent_mask)

    return image

def process_pdf(input_pdf_path, background_pdf_path, output_pdf_path):
    """
    Remove white background from each page of input PDF and overlay it on the background PDF.
    """
    input_pdf = fitz.open(input_pdf_path)
    background_pdf = fitz.open(background_pdf_path)

    if len(input_pdf) != len(background_pdf):
        raise ValueError("Both PDFs must have the same number of pages.")

    output_pdf = fitz.open()  # New empty PDF for output

    for page_num in range(len(input_pdf)):
        input_page = input_pdf.load_page(page_num)
        background_page = background_pdf.load_page(page_num)

        # Extract the image from the input PDF page
        zoom = 2  # Scale factor for higher resolution
        mat = fitz.Matrix(zoom, zoom)  # Create transformation matrix for zoom
        pix = input_page.get_pixmap(matrix=mat, alpha=True)
        extracted_img_path = f"extracted_page_{page_num}.png"
        pix.save(extracted_img_path)

        # Load the extracted image back as pixmap
        extracted_pix = fitz.Pixmap(extracted_img_path)

        # Create a new page in the output PDF with the background page dimensions
        output_page = output_pdf.new_page(width=background_page.rect.width, height=background_page.rect.height)

        # Draw the background page
        output_page.show_pdf_page(background_page.rect, background_pdf, page_num)

        # Overlay the extracted image on top of the background
        output_page.insert_image(output_page.rect, pixmap=extracted_pix)

        # Clean up temporary files
        # os.remove(img_path)
        os.remove(extracted_img_path)

    output_pdf.save(output_pdf_path)
    input_pdf.close()
    background_pdf.close()
    output_pdf.close()

def compress_pdf(input_file, output_file):
    try:
        # Define the Ghostscript command for compression
        gs_command = [
            'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/printer', '-dNOPAUSE', '-dBATCH', '-dQUIET',
            '-sOutputFile={}'.format(output_file), input_file
        ]
        
        # Execute the Ghostscript command
        subprocess.run(gs_command, check=True)
        print(f'Compressed PDF saved as: {output_file}')
    except subprocess.CalledProcessError as e:
        print(f'An error occurred: {e}')
    except FileNotFoundError:
        print('Ghostscript is not installed or not found in the system PATH.')

overlayed_pdf_path = "test_files/overlayed.pdf"
compressed_pdf_path = "test_files/compressed.pdf"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=multiline_description)
    parser.add_argument("foreground_pdf_path", help="Path to the input PDF with white background to remove.")
    parser.add_argument("background_pdf_path", help="Path to the background PDF to overlay the processed PDF onto.")
    parser.add_argument("output_pdf_path", help="Path to save the output PDF.")

    args = parser.parse_args()

# Overlay the 2 PDF files
process_pdf(args.foreground_pdf_path, args.background_pdf_path, overlayed_pdf_path)

# Compress the Overlayed PDF file.
compress_pdf(overlayed_pdf_path, args.output_pdf_path)

# Delete Overlayed PDF.
os.remove(overlayed_pdf_path)