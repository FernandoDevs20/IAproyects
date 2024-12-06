from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint

# Configuración general
MINIMUM_TWEETS = 100  # Cambiar según la cantidad de tweets deseada por tema

# Temas de búsqueda
QUERIES = [
    ('Ley del Poder Judicial', 'tweets_ley_poder_judicial.csv'),
    ('Reforma a los Organismos Autónomos', 'tweets_reforma_autonomos.csv')
]

# Leer credenciales desde config.ini
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

# Autenticación en X
client = Client(language='es-ES')
client.load_cookies('cookies.json')  # Cargar cookies si ya están guardadas
# client.login(auth_info_1=username, auth_info_2=email, password=password)
# client.save_cookies('cookies.json')

# Función para obtener tweets
def get_tweets(client, query, min_tweets, output_file):
    tweets = None
    tweet_count = 0

    # Crear el archivo CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])

    while tweet_count < min_tweets:
        try:
            if tweets is None:
                print(f"{datetime.now()} - Buscando tweets sobre '{query}'...")
                tweets = client.search_tweet(f'{query} lang:es', product='Top')
            else:
                wait_time = randint(5, 10)
                print(f"{datetime.now()} - Esperando {wait_time} segundos para buscar más tweets...")
                time.sleep(wait_time)
                tweets = tweets.next()

            # Guardar tweets
            for tweet in tweets:
                tweet_count += 1
                tweet_data = [
                    tweet_count,
                    tweet.user.name,
                    tweet.text,
                    tweet.created_at,
                    tweet.retweet_count,
                    tweet.favorite_count
                ]

                with open(output_file, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(tweet_data)

                if tweet_count >= min_tweets:
                    break

            print(f"{datetime.now()} - Total tweets encontrados: {tweet_count}")

        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f"{datetime.now()} - Límite de peticiones alcanzado. Esperando hasta {rate_limit_reset}...")
            wait_time = (rate_limit_reset - datetime.now()).total_seconds()
            time.sleep(wait_time)
            continue

        except Exception as e:
            print(f"{datetime.now()} - Error: {e}")
            break

    print(f"{datetime.now()} - Finalizado. Tweets guardados en '{output_file}'.")

# Ejecutar la extracción para cada tema
for query, output_file in QUERIES:
    get_tweets(client, query, MINIMUM_TWEETS, output_file)
