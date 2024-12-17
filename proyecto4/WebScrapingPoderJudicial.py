import requests
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Archivo de salida combinado
PODERJUDICIAL = "contenido_PODERJUDICIAL.txt"

# Configuración para Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecuta sin interfaz gráfica
chrome_options.add_argument("--disable-web-security")  # Desactiva la seguridad web
chrome_options.add_argument("--disable-gpu")  # Desactiva GPU
chrome_options.add_argument("--no-sandbox")  # Para entornos sin acceso privilegiado
service = Service("./chromedriver.exe")  # Ruta a chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)


pdf_links = [
    "https://www.gob.mx/cms/uploads/attachment/file/892010/REFORMA_AL_PODER_JUDICIAL__2_CS.pdf",
    "https://www.scjn.gob.mx/sites/default/files/agenda/documento/2024-09/reforma-integral-al-sistema-de-justicia-en-mexico.pdf",
    "https://www.scjn.gob.mx/sites/default/files/agenda/documento/2024-09/jornadas-nacionales-sobre-la-reforma-del-poder-judicial.pdf",
]

dynamic_links = [
    "https://cincodias.elpais.com/legal/2024-11-27/victor-olea-la-eleccion-popular-de-los-magistrados-en-mexico-implica-jueces-sumisos-al-poder-publico.html",
    "https://www.reformajudicial.gob.mx/secciones/reforma/",
    "https://www.diputados.gob.mx/LeyesBiblio/ref/lopjf.htm",
    "https://ibero.mx/prensa/mexico-atraviesa-una-crisis-constitucional-con-la-reforma-al-poder-judicial-especialistas",
    "https://www.dof.gob.mx/nota_detalle.php?codigo=5738985&fecha=15/09/2024#gsc.tab=0",
    "https://laverdadnoticias.com/politica/reforma-judicial-transparencia-y-disciplina-para-la-justicia-en-mexico-20241209",
    "https://elpais.com/mexico/2024-09-16/lopez-obrador-promulga-la-reforma-al-poder-judicial-que-somete-al-voto-popular-la-eleccion-de-los-jueces-en-mexico.html",
    "https://elpais.com/mexico/2024-12-10/norma-pina-lanza-su-critica-mas-dura-a-los-gobiernos-de-morena-se-nos-llamo-traidores-por-no-ser-parte-del-proyecto-politico-dominante.html",
    "https://elpais.com/mexico/2024-10-22/la-decision-de-una-jueza-de-frenar-la-reforma-judicial-lleva-al-limite-la-pugna-del-gobierno-de-sheinbaum-con-los-jueces.html",
    "https://mexicocomovamos.mx/publicaciones/2024/09/la-reforma-al-poder-judicial/",
    "https://agendaestadodederecho.com/jueces-sin-rostro-en-mexico/",   
    "https://animalpolitico.com/verificacion-de-hechos/te-explico/comites-evaluacion-reforma-judicial",
    "https://animalpolitico.com/verificacion-de-hechos/te-explico/comites-evaluacion-reforma-poder-judicial",
    "https://www.gob.mx/sspc/prensa/presentan-estrategia-para-frenar-violencia-politica-y-amenazas-a-candidatos?idiom=es",
    "https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S0188-76532012000100001",
    "https://insightcrime.org/es/noticias/como-planean-enfrentar-crimen-organizado-candidaturas-presidencia-mexico/"
    "https://elpais.com/mexico/2024-08-28/los-jueces-sin-rostro-la-nueva-polemica-en-torno-a-la-reforma-judicial-de-lopez-obrador.html",
    "https://cnnespanol.cnn.com/2024/09/13/que-son-jueces-sin-rostro-figuras-polemica-reforma-judicial-orix",
]

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
                driver.get(link)  # Abre el enlace
                title = driver.title  # Captura el título de la página
                
                # Captura encabezados H2, H3 y párrafos
                headers_h2 = driver.find_elements(By.TAG_NAME, "h2")
                headers_h3 = driver.find_elements(By.TAG_NAME, "h3")
                paragraphs = driver.find_elements(By.TAG_NAME, "p")
                
                # Escribe el título de la página
                combined_file.write(f"Título: {title}\n")
                
                # Escribe encabezados H2
                combined_file.write("Encabezados H2:\n")
                combined_file.write("\n".join([h2.text for h2 in headers_h2 if h2.text.strip()]) + "\n\n")
                
                # Escribe encabezados H3
                combined_file.write("Encabezados H3:\n")
                combined_file.write("\n".join([h3.text for h3 in headers_h3 if h3.text.strip()]) + "\n\n")
                
                # Escribe párrafos
                combined_file.write("Contenido:\n")
                combined_file.write("\n".join([p.text for p in paragraphs if p.text.strip()]) + "\n\n")
            
            except Exception as e:
                print(f"Error procesando {link}: {e}")

if __name__ == "__main__":
    # Vaciar archivo combinado antes de escribir
    with open(PODERJUDICIAL, "w", encoding="utf-8") as f:
        f.write("")

    print("Procesando PDFs...")
    process_pdf_links()
    print("Procesando enlaces dinámicos...")
    process_dynamic_links()
    driver.quit()

    print("Procesamiento completo. Todo el contenido se ha guardado en 'combined_content.txt'.")
