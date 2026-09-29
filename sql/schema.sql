-- =============================================================
-- SECCIÓN 2.1: Modelado de Datos (DDL)
-- =============================================================
-- Instrucciones:
-- Escribe las sentencias CREATE TABLE para almacenar 'desarrollos' y 'leads'.
-- Considera llaves primarias, foráneas, tipos de datos e índices recomendados.

CREATE TABLE desarrollos (
    id INT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL
);

CREATE TABLE leads (
    id INT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    telefono VARCHAR(30),
    origen VARCHAR(100) NOT NULL,
    campaña VARCHAR(100),
    fecha_registro DATETIME NOT NULL,
    estatus VARCHAR(50) NOT NULL,
    presupuesto DECIMAL(12, 2) DEFAULT 0,
    desarrollo_id INT NOT NULL,
    comentarios TEXT,
    FOREIGN KEY (desarrollo_id) REFERENCES desarrollos(id)
);

-- Crear tabla de desarrollos para tener información de los desarrollos

CREATE INDEX idx_leads_email ON leads(email);  -- estr es para el filtrado de leads por email
CREATE INDEX idx_leads_estatus ON leads(estatus); -- este es para el filtrado de leads por estatus
CREATE INDEX idx_leads_desarrollo ON leads(desarrollo_id); -- este es para el filtrado de leads por desarrollo
