import warnings
import requests
from bs4 import BeautifulSoup
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib3.exceptions import InsecureRequestWarning

# Desactivar advertencias de HTTPS no verificadas
warnings.simplefilter("ignore", InsecureRequestWarning)

# Archivos de salida
STATIC_CONTENT_FILE = "static_content.txt"
PDF_CONTENT_FILE = "pdf_content.txt"
DYNAMIC_CONTENT_FILE = "dynamic_content.txt"

# Configuración para Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecuta sin interfaz gráfica
chrome_options.add_argument("--ignore-certificate-errors")  # Ignorar errores de certificados
chrome_options.add_argument("--disable-web-security")  # Desactiva la seguridad web
chrome_options.add_argument("--disable-gpu")  # Desactiva GPU
chrome_options.add_argument("--no-sandbox")  # Para entornos sin acceso privilegiado
service = Service("./chromedriver.exe")  # Ruta a chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URLs categorizadas
static_links = [
    "https://cincodias.elpais.com/legal/2024-11-27/victor-olea-la-eleccion-popular-de-los-magistrados-en-mexico-implica-jueces-sumisos-al-poder-publico.html",
    "https://www.diputados.gob.mx/LeyesBiblio/ref/lopjf.htm"
]

pdf_links = [
    "https://www.gob.mx/cms/uploads/attachment/file/892010/REFORMA_AL_PODER_JUDICIAL__2_CS.pdf"
]

dynamic_links = [
    "https://comunicacionsocial.diputados.gob.mx/index.php/boletines/camara-de-diputados-avalo-en-lo-general-y-por-mayoria-calificada-reforma-constitucional-que-extingue-siete-organos-autonomos"
]

# Funciones para procesar las páginas (iguales que antes)
def process_static_links():
    for link in static_links:
        try:
            response = requests.get(link, verify=False)
            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find("title").text if soup.find("title") else "Sin título"
            paragraphs = soup.find_all("p")
            with open(STATIC_CONTENT_FILE, "a", encoding="utf-8") as file:
                file.write(f"URL: {link}\n")
                file.write(f"Título: {title}\n")
                file.write("Contenido:\n")
                for paragraph in paragraphs:
                    file.write(paragraph.text + "\n")
                file.write("\n\n")
        except Exception as e:
            print(f"Error procesando {link}: {e}")

def process_pdf_links():
    for link in pdf_links:
        try:
            response = requests.get(link, verify=False)
            pdf_path = "temp.pdf"
            with open(pdf_path, "wb") as file:
                file.write(response.content)
            with pdfplumber.open(pdf_path) as pdf:
                content = "".join([page.extract_text() for page in pdf.pages])
            with open(PDF_CONTENT_FILE, "a", encoding="utf-8") as file:
                file.write(f"URL: {link}\n")
                file.write("Contenido:\n")
                file.write(content + "\n\n")
        except Exception as e:
            print(f"Error procesando {link}: {e}")

def process_dynamic_links():
    for link in dynamic_links:
        try:
            driver.get(link)
            title = driver.title
            paragraphs = driver.find_elements(By.TAG_NAME, "p")
            content = "\n".join([p.text for p in paragraphs])
            with open(DYNAMIC_CONTENT_FILE, "a", encoding="utf-8") as file:
                file.write(f"URL: {link}\n")
                file.write(f"Título: {title}\n")
                file.write("Contenido:\n")
                file.write(content + "\n\n")
        except Exception as e:
            print(f"Error procesando {link}: {e}")

if __name__ == "__main__":
    print("Procesando enlaces estáticos...")
    process_static_links()
    print("Procesando PDFs...")
    process_pdf_links()
    print("Procesando enlaces dinámicos...")
    process_dynamic_links()
    driver.quit()
    print("Procesamiento completo. Contenido guardado en archivos de texto.")
