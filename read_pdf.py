import PyPDF2
import sys

# Set UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

# Read the PDF
pdf_path = r'c:\Users\nduta\OneDrive\Desktop\Projects\nonlist\Project 2 Instructions Fall 2025.pdf'
with open(pdf_path, 'rb') as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() + '\n'
    
    print(text)
