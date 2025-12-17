CREATE TABLE road_sections (
    section_id TEXT PRIMARY KEY,
    road_number INT,
    road_type TEXT,
    coords_json TEXT
);

CREATE TABLE road_forecasts (
    section_id TEXT REFERENCES road_sections(section_id),
    forecast_time TIMESTAMPTZ,
    forecast_name TEXT,
    forecast_type TEXT,             
    overall_road_condition TEXT,
    precipitation_condition TEXT,
    road_temperature FLOAT,
    air_temperature FLOAT,
    wind_speed FLOAT,
    wind_direction INT,
    daylight BOOLEAN,
    reliability TEXT,
    data_updated_time TEXT,
    weather_symbol TEXT,             
    road_condition TEXT,             
    PRIMARY KEY (section_id, forecast_time)
);
