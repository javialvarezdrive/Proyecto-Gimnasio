-- Tabla para monitores (usuarios que usan la webapp)
CREATE TABLE monitors (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL  -- Recuerda: en producción almacenar el hash de la contraseña
);

-- Tabla para los miembros del gimnasio (alumnos)
CREATE TABLE gym_members (
    id SERIAL PRIMARY KEY,
    nip INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    seccion TEXT NOT NULL CHECK (seccion IN ('SETRA', 'Motorista', 'GOA', 'Patrullas')),
    grupo TEXT NOT NULL CHECK (grupo IN ('G-1', 'G-2', 'G-3'))
);

-- Tabla para las actividades disponibles.
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT
);

-- Inserción de actividades por defecto (opcional)
INSERT INTO activities (nombre, descripcion)
VALUES 
('Defensa Personal', 'Actividad de defensa personal'),
('Acondicionamiento Físico', 'Actividad de acondicionamiento físico');

-- Tabla para registrar el agendamiento de actividades
CREATE TABLE schedule (
    id SERIAL PRIMARY KEY,
    member_id INTEGER REFERENCES gym_members(id),
    activity_id INTEGER REFERENCES activities(id),
    fecha DATE NOT NULL,
    turno TEXT NOT NULL CHECK (turno IN ('Mañana','Tarde','Noche')),
    monitor_id INTEGER REFERENCES monitors(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
