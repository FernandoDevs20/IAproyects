import pdfplumber
import requests

# Lista de enlaces a PDFs
pdf_links = [
    "https://www.gob.mx/cms/uploads/attachment/file/892010/REFORMA_AL_PODER_JUDICIAL__2_CS.pdf",
    "http://congresomich.gob.mx/file/LEY-ORG%C3%81NICA-DEL-PODER-JUDICIAL-REF-5-DE-JULIO-DE-2023.pdf"
]

for link in pdf_links:
    response = requests.get(link)
    pdf_path = "temp.pdf"
    
    # Guardar el PDF temporalmente
    with open(pdf_path, "wb") as file:
        file.write(response.content)
    
    # Extraer contenido del PDF
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    
    # Guardar el contenido extraído
    with open("pdf_content.txt", "a", encoding="utf-8") as file:
        file.write(f"URL: {link}\n")
        file.write("Contenido:\n")
        file.write(text + "\n\n")
