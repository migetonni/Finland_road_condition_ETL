--road sections dimension table

CREATE TABLE road_sections (
    section_id TEXT PRIMARY KEY,
    road_number INT,
    road_type TEXT,
    coords_json TEXT
);

--domain tables
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
--forecast fact table

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

--table for historical conditions
CREATE TABLE historical_road_conditions(
    section_id TEXT,
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
    PRIMARY KEY (section_id, forecast_time)

);

--table for etl run logging
CREATE TABLE etl_runs (
    run_id TEXT PRIMARY KEY,
    flow_name TEXT,

    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,

    status TEXT CHECK (status IN ('SUCCESS', 'FAILED')),

    duration_seconds INT,

    error_message TEXT
);



-- Analytics view

CREATE OR REPLACE VIEW powerbi_road_conditions AS
SELECT
  rf.section_id,
  rf.forecast_time,
  rf.forecast_name,
  rf.forecast_type,

  rf.overall_road_condition,
  rf.precipitation_condition,
  rf.road_condition,
  rf.reliability,

  rf.road_temperature,
  rf.air_temperature,
  rf.wind_speed,
  rf.wind_direction,
  rf.daylight,

  rf.weather_symbol,
  rf.data_updated_time,

  rs.road_number,
  rs.road_type,
  rs.coords_json

FROM road_forecasts rf
JOIN road_sections rs
  ON rf.section_id = rs.section_id;



