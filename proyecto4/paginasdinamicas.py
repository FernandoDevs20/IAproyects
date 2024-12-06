from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configuración de Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service("path/to/chromedriver")  # Cambia esta ruta por la de tu ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Lista de enlaces dinámicos
dynamic_links = [
    "https://comunicacionsocial.diputados.gob.mx/index.php/boletines/camara-de-diputados-avalo-en-lo-general-y-por-mayoria-calificada-reforma-constitucional-que-extingue-siete-organos-autonomos",
    "https://apnews.com/article/mexico-senado-reforma-constitucion-autonomos-c9fc664aa4a675d7de2948025b5dbf5f"
]

for link in dynamic_links:
    driver.get(link)
    
    # Extraer título
    title = driver.title
    
    # Extraer párrafos
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    content = "\n".join([p.text for p in paragraphs])
    
    # Guardar el contenido extraído
    with open("dynamic_content.txt", "a", encoding="utf-8") as file:
        file.write(f"URL: {link}\n")
        file.write(f"Título: {title}\n")
        file.write("Contenido:\n")
        file.write(content + "\n\n")

driver.quit()
