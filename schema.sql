CREATE TABLE road_sections (
    section_id TEXT PRIMARY KEY,
    road_number INT,
    road_type TEXT,
    coords_json TEXT
);

CREATE TABLE precipitation_types (
    precipitation_condition TEXT PRIMARY KEY
);

CREATE TABLE road_condition_types (
    road_condition TEXT PRIMARY KEY
);

CREATE TABLE overall_road_condition_types (
    overall_road_condition TEXT PRIMARY KEY
);

CREATE TABLE reliability_types (
    reliability TEXT PRIMARY KEY
);

CREATE TABLE road_forecasts (
    section_id TEXT REFERENCES road_sections(section_id),
    forecast_time TIMESTAMPTZ,
    forecast_name TEXT,
    forecast_type TEXT,             
    overall_road_condition TEXT REFERENCES overall_road_condition_types(overall_road_condition),
    precipitation_condition TEXT REFERENCES precipitation_types(precipitation_condition),
    road_temperature FLOAT,
    air_temperature FLOAT,
    wind_speed FLOAT,
    wind_direction INT,
    daylight BOOLEAN,
    reliability TEXT REFERENCES reliability_types(reliability),
    data_updated_time TEXT,
    weather_symbol TEXT,             
    road_condition TEXT REFERENCES road_condition_types(road_condition),
    PRIMARY KEY (section_id, forecast_time, road_condition)
);


