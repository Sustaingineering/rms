CREATE TABLE IF NOT EXISTS sensor_readings (
    id SERIAL PRIMARY KEY,
    timestamp DOUBLE PRECISION NOT NULL,
    ina_current DOUBLE PRECISION,
    ina_voltage DOUBLE PRECISION,
    rpm DOUBLE PRECISION,
    lg_avg_speed DOUBLE PRECISION,
    wind_power DOUBLE PRECISION
);