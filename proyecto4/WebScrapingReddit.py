import praw

# Archivos de salida
REDDIT_JUDICIAL_FILE = "reddit_ley_poder_judicial.txt"
REDDIT_AUTONOMOS_FILE = "reddit_reforma_organismos_autonomos.txt"

# Configuración de Reddit
reddit = praw.Reddit(
                    client_id='VGNhK2YbieqKfOMq9Eu_gQ',
                    client_secret='RmCyNXSXA1TcRFl9oq0gChtpHC0VYw',
                    user_agent='Prueba'
)

# Función para guardar datos en archivo
def save_to_file(filename, data):
    with open(filename, "a", encoding="utf-8") as file:
        file.write(data + "\n\n")

# Procesar datos de Reddit
def fetch_reddit_data(query, filename):
    print(f"Buscando en Reddit: {query}")
    for submission in reddit.subreddit('all').search(query, limit=1000):
        data = f"Título: {submission.title}\nContenido: {submission.selftext}"
        save_to_file(filename, data)

if __name__ == "__main__":
    # Temas y sus archivos correspondientes
    topics = [
        ("Ley del Poder Judicial", REDDIT_JUDICIAL_FILE),
        ("Reforma a los Organismos Autónomos", REDDIT_AUTONOMOS_FILE)
    ]
    
    # Procesar cada tema
    for topic, reddit_file in topics:
        fetch_reddit_data(topic, reddit_file)
    
    print("Extracción completa. Datos guardados en archivos.")
