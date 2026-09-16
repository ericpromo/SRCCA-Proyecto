import feedparser
import hashlib
from datetime import datetime, timezone
from bs4 import BeautifulSoup

def limpiar_html(contenido_html):
    """Extrae el texto limpio de un contenido HTML usando BeautifulSoup."""
    soup = BeautifulSoup(contenido_html, 'html.parser')
    return soup.get_text().strip()

def generar_hash(contenido):
    """Genera un hash SHA-256 único para detectar contenido duplicado."""
    return hashlib.sha256(contenido.encode('utf-8')).hexdigest()

def normalizar_fecha(entrada_feed):
    """Convierte la fecha ya parseada por feedparser en un datetime real"""
    tiempo_struct = entrada_feed.published_parsed
    return datetime(*tiempo_struct[:6], tzinfo=timezone.utc)

def obtener_articulos_limpios():
    """Descarga el feed RSS, limpia cada artículo, y devuelve la lista lista para usar."""
    url = "https://feeds.feedburner.com/TheHackersNews"
    feed = feedparser.parse(url)

    articulos_limpios = []
    for entrada in feed.entries:
        contenido_limpio = limpiar_html(entrada.summary)
        articulo = {
            "titulo": entrada.title.strip(),
            "link": entrada.link,
            "fecha_publicacion": normalizar_fecha(entrada),
            "contenido_limpio": contenido_limpio,
            "hash_contenido": generar_hash(contenido_limpio)
        }
        articulos_limpios.append(articulo)

    return articulos_limpios

#  Esto solo corre si ejecutás ESTE archivo directamente 
if __name__ == "__main__":
    articulos = obtener_articulos_limpios()
    print(f"Se han extraído {len(articulos)} artículos en total.")
    print("\n---Ejemplo del primer artículo saneado---")
    print(articulos[0])