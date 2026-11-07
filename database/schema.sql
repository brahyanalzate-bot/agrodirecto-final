CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE productores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    origen_registro TEXT CHECK (origen_registro IN ('DATOS_GOV', 'WHATSAPP', 'WEB')),
    nombre_asociacion TEXT,
    contacto_nombre TEXT NOT NULL,
    telefono TEXT UNIQUE NOT NULL,
    identificador_fiscal TEXT,
    departamento TEXT,
    municipio TEXT,
    ubicacion GEOMETRY(Point, 4326),
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE cosechas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    productor_id UUID REFERENCES productores(id) ON DELETE CASCADE,
    producto TEXT NOT NULL,
    variedad TEXT,
    calidad_grado TEXT CHECK (calidad_grado IN ('PRIMERA', 'SEGUNDA', 'INDUSTRIAL')),
    volumen_kg DECIMAL NOT NULL,
    precio_kilo_estimado DECIMAL NOT NULL,
    fecha_disponibilidad DATE NOT NULL,
    estado TEXT DEFAULT 'DISPONIBLE' CHECK (estado IN ('DISPONIBLE', 'RESERVADO', 'AGOTADO')),
    imagenes_urls JSONB,
    ubicacion_acopio GEOMETRY(Point, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE compradores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    razon_social TEXT NOT NULL,
    tipo_comprador TEXT CHECK (tipo_comprador IN ('HORECA', 'MAYORISTA', 'SUPERMERCADO', 'PARTICULAR')),
    telefono TEXT,
    email TEXT UNIQUE,
    ubicacion GEOMETRY(Point, 4326)
);

CREATE TABLE transacciones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cosecha_id UUID REFERENCES cosechas(id),
    comprador_id UUID REFERENCES compradores(id),
    productor_id UUID REFERENCES productores(id),
    volumen_acordado_kg DECIMAL NOT NULL,
    monto_total DECIMAL NOT NULL,
    estado_pago TEXT CHECK (estado_pago IN ('PENDIENTE_ESCROW', 'FONDOS_RETENIDOS', 'PAGADO_AL_PRODUCTOR', 'CANCELADO')),
    fecha_transaccion TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE reputacion_resenas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaccion_id UUID UNIQUE REFERENCES transacciones(id),
    calificador_id UUID,
    calificado_id UUID,
    puntuacion INTEGER CHECK (puntuacion BETWEEN 1 AND 5),
    comentario TEXT,
    puntualidad_entrega SMALLINT CHECK (puntualidad_entrega BETWEEN 1 AND 5),
    calidad_producto_fidelidad SMALLINT CHECK (calidad_producto_fidelidad BETWEEN 1 AND 5),
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE MATERIALIZED VIEW mv_productor_score AS
SELECT p.id as productor_id, COUNT(r.id) as total_resenas, AVG(r.puntuacion) as avg_stars,
(COUNT(CASE WHEN r.puntuacion >= 4 THEN 1 END)::FLOAT / NULLIF(COUNT(r.id), 0)) * 100 as tasa_cumplimiento
FROM productores p LEFT JOIN reputacion_resenas r ON p.id = r.calificado_id GROUP BY p.id;
