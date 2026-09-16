from ingesta.ingesta import obtener_articulos_limpios
from ia.analizador import analizar_articulo

articulos = obtener_articulos_limpios()
print(f"Se trajeron {len(articulos)} artículos de la fuente.\n")

# Pruebo con uno solo primero, para no gastar cuota de la API de golpe
primero = articulos[0]
print(f"Analizando: {primero['titulo']}\n")

analisis = analizar_articulo(primero["contenido_limpio"])

print(f"Severidad: {analisis.severidad}")
print(f"Resumen: {analisis.resumen_ejecutivo}")
for af in analisis.afectaciones:
    print(f"  - {af.tecnologia_afectada}: {af.vector_ataque}")