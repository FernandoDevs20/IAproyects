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

# Archivo de salida combinado
PODERJUDICIAL = "contenido_poderjudicial.txt"

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
    "https://www.diputados.gob.mx/LeyesBiblio/ref/lopjf.htm",
    "https://www.reformajudicial.gob.mx/secciones/reforma/",
    "https://www.dof.gob.mx/nota_detalle.php?codigo=5738985&fecha=15/09/2024#gsc.tab=0",
    "https://ibero.mx/prensa/mexico-atraviesa-una-crisis-constitucional-con-la-reforma-al-poder-judicial-especialistas"
]

pdf_links = [
    "https://www.gob.mx/cms/uploads/attachment/file/892010/REFORMA_AL_PODER_JUDICIAL__2_CS.pdf",
    "https://www.scjn.gob.mx/sites/default/files/agenda/documento/2024-09/reforma-integral-al-sistema-de-justicia-en-mexico.pdf",
    "https://www.scjn.gob.mx/sites/default/files/agenda/documento/2024-09/jornadas-nacionales-sobre-la-reforma-del-poder-judicial.pdf",
]

dynamic_links = [
    "https://laverdadnoticias.com/politica/reforma-judicial-transparencia-y-disciplina-para-la-justicia-en-mexico-20241209",
    "https://elpais.com/mexico/2024-09-16/lopez-obrador-promulga-la-reforma-al-poder-judicial-que-somete-al-voto-popular-la-eleccion-de-los-jueces-en-mexico.html",
    "https://elpais.com/mexico/2024-12-10/norma-pina-lanza-su-critica-mas-dura-a-los-gobiernos-de-morena-se-nos-llamo-traidores-por-no-ser-parte-del-proyecto-politico-dominante.html?",
    "https://eljuegodelacorte.nexos.com.mx/el-abc-de-la-reforma-a-los-organismos-autonomos/"
]

# Procesar enlaces estáticos
def process_static_links():
    with open(PODERJUDICIAL, "a", encoding="utf-8") as combined_file:
        combined_file.write("### Contenido Estático ###\n")
        for link in static_links:
            try:
                response = requests.get(link, verify=False)
                soup = BeautifulSoup(response.content, "html.parser")
                title = soup.find("title").text if soup.find("title") else "Sin título"
                paragraphs = soup.find_all("p")
                combined_file.write(f"Título: {title}\n")
                combined_file.write("Contenido:\n")
                for paragraph in paragraphs:
                    combined_file.write(paragraph.text + "\n")
                combined_file.write("\n\n")
            except Exception as e:
                print(f"Error procesando {link}: {e}")

# Procesar PDFs
def process_pdf_links():
    with open(PODERJUDICIAL, "a", encoding="utf-8") as combined_file:
        combined_file.write("### Contenido de PDFs ###\n")
        for link in pdf_links:
            try:
                response = requests.get(link, verify=False)
                pdf_path = "temp.pdf"
                with open(pdf_path, "wb") as file:
                    file.write(response.content)
                with pdfplumber.open(pdf_path) as pdf:
                    content = "".join([page.extract_text() for page in pdf.pages if page.extract_text()])
                combined_file.write("Contenido:\n")
                combined_file.write(content + "\n\n")
            except Exception as e:
                print(f"Error procesando {link}: {e}")

# Procesar enlaces dinámicos
def process_dynamic_links():
    with open(PODERJUDICIAL, "a", encoding="utf-8") as combined_file:
        combined_file.write("### Contenido Dinámico ###\n")
        for link in dynamic_links:
            try:
                driver.get(link)
                title = driver.title
                paragraphs = driver.find_elements(By.TAG_NAME, "p")
                content = "\n".join([p.text for p in paragraphs])
                combined_file.write(f"Título: {title}\n")
                combined_file.write("Contenido:\n")
                combined_file.write(content + "\n\n")
            except Exception as e:
                print(f"Error procesando {link}: {e}")

if __name__ == "__main__":
    # Vaciar archivo combinado antes de escribir
    with open(PODERJUDICIAL, "w", encoding="utf-8") as f:
        f.write("")

    print("Procesando enlaces estáticos...")
    process_static_links()
    print("Procesando PDFs...")
    process_pdf_links()
    print("Procesando enlaces dinámicos...")
    process_dynamic_links()
    driver.quit()

    print("Procesamiento completo. Todo el contenido se ha guardado en 'combined_content.txt'.")
