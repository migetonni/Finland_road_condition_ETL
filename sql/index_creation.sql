CREATE INDEX idx_road_sections_road_type
ON road_sections (road_type);

CREATE INDEX idx_road_forecast_section_id
ON road_forecasts (section_id);

CREATE INDEX idx_road_forecasts_forecast_time
ON road_forecasts (forecast_time);

CREATE INDEX idx_historical_road_conditions_time
ON historical_road_conditions (forecast_time);

