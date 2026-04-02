import pdfplumber

# Open the CV file
with pdfplumber.open("../data/sample_cv.pdf") as pdf:
    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

# Print the extracted text
print(text)