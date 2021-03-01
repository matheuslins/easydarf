

def save_pdf(pdf_string: str, _id: str):
    file_name = f'darf_{_id}.pdf'
    with open(file_name, 'wb') as f:
        f.write(pdf_string.encode())
