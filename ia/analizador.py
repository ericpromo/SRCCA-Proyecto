# ia/analizador.py
import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel
from typing import Literal, List

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class Afectacion(BaseModel):
    tecnologia_afectada: str
    vector_ataque: str

class AnalisisAlerta(BaseModel):
    severidad: Literal["Baja", "Media", "Alta", "Critica"]
    resumen_ejecutivo: str
    afectaciones: List[Afectacion]

def analizar_articulo(contenido_limpio: str) -> AnalisisAlerta:
    prompt = f"""
    Sos un analista de ciberseguridad. Analizá el siguiente artículo
    y extraé la información en el formato solicitado.

    Reglas importantes:
    - El resumen_ejecutivo debe estar redactado en español, aunque el
      artículo original esté en inglés.
    - Identificá cada tecnología/sistema afectado por separado, con su
      propio vector de ataque específico.
    - La severidad debe reflejar el impacto real descrito en el texto.

    Artículo:
    {contenido_limpio}
    """
    respuesta = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={"response_mime_type": "application/json", "response_schema": AnalisisAlerta},
    )
    return respuesta.parsed

#  Esto solo corre si ejecutás ESTE archivo directamente, no cuando lo importás 
if __name__ == "__main__":
    texto_de_prueba = """
    A critical vulnerability was discovered in Apache Log4j allowing
    remote code execution. Attackers can exploit this via crafted
    JNDI lookups, affecting servers running Log4j 2.x.
    """
    resultado = analizar_articulo(texto_de_prueba)
    print(f"Severidad: {resultado.severidad}")
    print(f"Resumen: {resultado.resumen_ejecutivo}")
    for af in resultado.afectaciones:
        print(f"  - {af.tecnologia_afectada}: {af.vector_ataque}")