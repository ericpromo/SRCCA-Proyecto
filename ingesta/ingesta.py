import feedparser
import hashlib
from datetime import datetime, timezone
from bs4 import BeautifulSoup

def limpiar_html(contenido_html):
    """Extrae el texto limpio de un contenido HTML usando BeautifulSoup."""
    soup = BeautifulSoup(contenido_html, 'html.parser')
    return soup.get_text().strip()

def generar_hash(contenido):
    """Genera un has SHA-256 unico para detectar contenido duplicado."""
    return hashlib.sha256(contenido.encode('utf-8')).hexdigest()

def normalizar_fecha(entrada_feed):
    """Convierte la fecha ya parseada por feedparser en un datetime real"""
    tiempo_struct = entrada_feed.published_parsed
    return datetime(*tiempo_struct[:6], tzinfo=timezone.utc)  # Convertir a UTC



#URL del feed RSS de The Hacker News
url = "https://feeds.feedburner.com/TheHackersNews"

feed = feedparser.parse(url)

# print(f"Titulo del feed: {feed.feed.title}")
# print(f"Cantidad de articulos encontrados: {len(feed.entries)}")

# # Mostar el primer articulo como prueba
# primero = feed.entries[0]
# print("\n---Primer Articulo---")
# print(f"Titulo: {primero.title}")
# print(f"Link: {primero.link}")
# print(f"Fecha: {primero.published}")
# print(f"Resumen: {primero.summary[:200]}") # solo los primeros 200 caracteres

articulos = []

for entrada in feed.entries:
    articulo = {
        "titulo": entrada.title,
        "link": entrada.link,
        "fecha_publicacion": entrada.published,
        "contenido_crudo": entrada.summary
    }
    articulos.append(articulo)

print(f"Se han extraido {len(articulos)} articulos en total.")
print("\n---Ejemplo del segundo articulo guardado---")
print(articulos[1])  # Mostrar el segundo artículo como ejemplo