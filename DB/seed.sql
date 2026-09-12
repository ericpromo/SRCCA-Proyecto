
--Ctrl E 2 veces para ejecutar solo lo que yo seleccione

--1. Prueba Tabla Fuente
INSERT INTO fuentes (nombre, url_base, tipo)
VALUES ('The Hacker News', 'https://thehackernews.com', 'RSS')
RETURNING id;


--2. Prueba Alerta
INSERT INTO alertas (fuente_id, titulo, contenido_limpio, fecha_publicacion, hash_contenido, severidad, resumen_ejecutivo)
VALUES (
    1,
    'Vulnerabilidad crítica en Log4j permite ejecución remota de código',
    'Se ha descubierto una falla en la librería Log4j que permite...',
    '2026-09-09 10:30:00',
    'a3f5c9d8e1b2test',
    'Critica',
    'La vulnerabilidad CVE-2021-44228 afecta múltiples sistemas basados en Java.'
)
RETURNING id;

--3. Prueba Afectación
INSERT INTO afectaciones (alerta_id, tecnologia_afectada, vector_ataque, parche_disponible, parche_referencia)
VALUES
    (1, 'Apache Log4j 2.x', 'RCE (Remote Code Execution)', TRUE, 'Log4j 2.17.1'),
    (1, 'Servidores Minecraft con Log4j embebido', 'RCE via JNDI', TRUE, 'Actualizar a versión parcheada del launcher');


-- JOIN de tablas
SELECT
    a.titulo,
    a.severidad,
    f.nombre AS fuente,
    af.tecnologia_afectada,
    af.vector_ataque
FROM alertas a
JOIN fuentes f ON a.fuente_id = f.id
JOIN afectaciones af ON a.id = af.alerta_id;

-- Prueba  1: Violar UNIQUE (mismo hash_contenido que ya existe)
INSERT INTO alertas (fuente_id, titulo, contenido_limpio, fecha_publicacion, hash_contenido, severidad, resumen_ejecutivo)
VALUES (
    1,
    'Alerta duplicada de prueba',
    'Contenido de prueba',
    '2026-09-11 12:00:00',
    'a3f5c9d8e1b2test', -- mismo hash que la alerta ya insertada
    'Alta',
    'Esto debería fallar por UNIQUE'
);

-- Prueba 2: violar CHECK ( severidad fuera de los valores permitidos) 
INSERT INTO alertas (fuente_id, titulo, contenido_limpio, fecha_publicacion, hash_contenido, severidad, resumen_ejecutivo)
VALUES (
    1,
    'Alerta con severidad inválida',
    'Contenido de prueba',
    '2026-09-11 12:00:00',
    'hash_distinto_001',
    'Urgente', -- no está en la lista ('Baja','Media','Alta','Critica')
    'Esto debería fallar por CHECK'
);

-- Prueba 3: violar FOREIGN KEY (alerta_id que no existe)
INSERT INTO afectaciones (alerta_id, tecnologia_afectada, vector_ataque, parche_disponible, parche_referencia)
VALUES (
    999, -- no existe ninguna alerta con este id
    'Sistema inventado',
    'Vector de prueba',
    FALSE,
    NULL
);