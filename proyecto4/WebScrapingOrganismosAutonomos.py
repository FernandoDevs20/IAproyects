import requests
import pdfplumber
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Archivo de salida combinado
ORGANISMOSAUTONOMOS = "contenido_organismosautonomos.txt"

# Configuración para Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecuta sin interfaz gráfica
chrome_options.add_argument("--ignore-certificate-errors")  # Ignorar errores de certificados
chrome_options.add_argument("--disable-web-security")  # Desactiva la seguridad web
chrome_options.add_argument("--disable-gpu")  # Desactiva GPU
chrome_options.add_argument("--no-sandbox")  # Para entornos sin acceso privilegiado
service = Service("./chromedriver.exe")  # Ruta a chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)


pdf_links = [
    "https://media.datacivica.org/pdf/analisis_propuesta_reforma_constitucional_oca.pdf",
    "https://gaceta.diputados.gob.mx/PDF/65/2024/feb/20240205-18.pdf",
    "https://archivos.juridicas.unam.mx/www/bjv/libros/1/306/7.pdf",
    "https://escuelajudicial.cjf.gob.mx/publicaciones/revista/29/Filiberto%20Valent%C3%ADn%20Ugalde%20Calder%C3%B3n.pdf",

]

dynamic_links = [
    "https://comunicacionsocial.diputados.gob.mx/index.php/boletines/camara-de-diputados-avalo-en-lo-general-y-por-mayoria-calificada-reforma-constitucional-que-extingue-siete-organos-autonomos",
    "https://cnnespanol.cnn.com/2024/11/29/senado-mexico-aprueba-reforma-eliminacion-siete-organos-autonomos-orix",
    "https://sistemamexiquense.mx/noticia/camara-diputados-declara-constitucional-extincion-inai-otros-organismos-autonomos",
    "https://eljuegodelacorte.nexos.com.mx/el-abc-de-la-reforma-a-los-organismos-autonomos/"
    "https://elpais.com/mexico/2024-11-29/el-senado-extermina-siete-organos-y-entes-autonomos-incluido-el-inai.html"
    "https://www.jornada.com.mx/noticia/2024/11/20/politica/aprueban-en-lo-general-reforma-para-desaparecer-organismos-autonomos-1414",
    "https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S1405-91932017000200085",
    "https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S2448-57052022000200315",
    "https://revistas-colaboracion.juridicas.unam.mx/index.php/opera-prima-derecho-admin/article/download/1573/1472",
]

# Procesar PDFs
def process_pdf_links():
    with open(ORGANISMOSAUTONOMOS, "a", encoding="utf-8") as combined_file:
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
    with open(ORGANISMOSAUTONOMOS, "a", encoding="utf-8") as combined_file:
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
    with open(ORGANISMOSAUTONOMOS, "w", encoding="utf-8") as f:
        f.write("")

    print("Procesando PDFs...")
    process_pdf_links()
    print("Procesando enlaces dinámicos...")
    process_dynamic_links()
    driver.quit()

    print("Procesamiento completo. Todo el contenido se ha guardado en 'combined_content.txt'.")
