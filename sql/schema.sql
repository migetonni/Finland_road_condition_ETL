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
    PRIMARY KEY (section_id, forecast_time, forecast_type)
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
    road_condition TEXT REFERENCES road_condition_types(road_condition)
    

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

--datetime dimension table

CREATE TABLE datetime (
    datetime_key INTEGER PRIMARY KEY,
    full_timestamp TIMESTAMPTZ NOT NULL UNIQUE,
    date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    week INTEGER NOT NULL,
    day INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name TEXT NOT NULL,
    hour INTEGER NOT NULL,
    is_weekend BOOLEAN NOT NULL
);

--filling dimension table
INSERT INTO datetime
SELECT
    ROW_NUMBER() OVER () AS datetime_key,
    ts,
    ts::date,
    EXTRACT(YEAR FROM ts)::int,
    EXTRACT(QUARTER FROM ts)::int,
    EXTRACT(MONTH FROM ts)::int,
    TO_CHAR(ts, 'Month'),
    EXTRACT(WEEK FROM ts)::int,
    EXTRACT(DAY FROM ts)::int,
    EXTRACT(DOW FROM ts)::int,
    TO_CHAR(ts, 'Day'),
    EXTRACT(HOUR FROM ts)::int,
    EXTRACT(DOW FROM ts) IN (0,6)
FROM generate_series(
    '2025-01-01 00:00:00+00'::timestamptz,
    '2027-12-31 23:00:00+00'::timestamptz,
    INTERVAL '1 hour'
) AS ts;


-- adding datetime_key to fact tables and making relationship to datetime table
ALTER TABLE road_forecasts
ADD COLUMN datetime_key INTEGER;

UPDATE road_forecasts rf
SET datetime_key = dt.datetime_key
FROM datetime dt
WHERE rf.forecast_time = dt.full_timestamp;

ALTER TABLE road_forecasts
ADD CONSTRAINT fk_datetime
FOREIGN KEY (datetime_key)
REFERENCES datetime(datetime_key);


ALTER TABLE historical_road_conditions
ADD COLUMN datetime_key INTEGER;

UPDATE historical_road_conditions hr
SET datetime_key = dt.datetime_key
FROM datetime dt
WHERE hr.forecast_time = dt.full_timestamp;

ALTER TABLE historical_road_conditions
ADD CONSTRAINT fk_datetime
FOREIGN KEY (datetime_key)
REFERENCES datetime(datetime_key);

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



