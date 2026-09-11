-- Tabla 1: Fuentes de información (ej. The Hacker News, feeds RSS)
CREATE TABLE fuentes (
    id          SERIAL PRIMARY KEY,
    nombre      VARCHAR(150) NOT NULL,
    url_base    VARCHAR(255) NOT NULL UNIQUE,
    tipo        VARCHAR(50)  NOT NULL
);

-- Tabla 2: Alertas de seguridad (el núcleo del sistema)
CREATE TABLE alertas (
    id                  SERIAL PRIMARY KEY,
    fuente_id           INT NOT NULL REFERENCES fuentes(id),
    titulo              VARCHAR(255) NOT NULL,
    contenido_limpio    TEXT,
    fecha_publicacion   TIMESTAMP NOT NULL,
    hash_contenido      VARCHAR(64) UNIQUE NOT NULL,
    severidad           VARCHAR(20) NOT NULL
                         CHECK (severidad IN ('Baja','Media','Alta','Critica')),
    resumen_ejecutivo   TEXT,
    estado              BOOLEAN DEFAULT TRUE
);

-- Tabla 3: Afectaciones (tecnologías/sistemas impactados por cada alerta)
CREATE TABLE afectaciones (
    id                   SERIAL PRIMARY KEY,
    alerta_id            INT NOT NULL REFERENCES alertas(id),
    tecnologia_afectada  VARCHAR(150) NOT NULL,
    vector_ataque        VARCHAR(100),
    parche_disponible    BOOLEAN DEFAULT FALSE,
    parche_referencia    TEXT
);