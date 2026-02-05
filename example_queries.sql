--Example of some analytical SQL queries made on the data produced by the pipeline

--Distribution of road conditions
SELECT
  road_condition,
  COUNT(*) AS count
FROM road_forecasts
GROUP BY road_condition
ORDER BY count DESC;

--Average road temperature for each road type
SELECT
  rs.road_type,
  AVG(rf.road_temperature) AS avg_road_temp
FROM road_forecasts rf
JOIN road_sections rs
  ON rf.section_id = rs.section_id
GROUP BY rs.road_type;

--The amount of realible and unreliable forecasts
SELECT
  reliability,
  COUNT(*) AS forecasts
FROM road_forecasts
GROUP BY reliability;

--Wet, Snowy or icy conditions by road type
SELECT
  rs.road_type,
  rf.road_condition,
  COUNT(*) AS count
FROM road_forecasts rf
JOIN road_sections rs USING (section_id)
WHERE rf.road_condition IN ('WET', 'ICE', 'SNOW')
GROUP BY rs.road_type, rf.road_condition;

--Percentage of all roads that are in good and bad condition
SELECT
  ROUND(
    100.0 * SUM(
      CASE
        WHEN road_condition IN ('WET', 'ICE', 'SNOW', 'SLUSH', 'MOIST')
        THEN 1 ELSE 0
      END
    ) / COUNT(*),
    2
  ) AS bad_cond_percentage,
  ROUND(
    100.0 * SUM(
      CASE
        WHEN road_condition IN ('WET', 'ICE', 'SNOW', 'SLUSH', 'MOIST')
        THEN 0 ELSE 1
      END
    ) / COUNT(*),
    2
  ) AS good_cond_percentage


FROM road_forecasts;

--Percentage of all roads that are in good and bad condition by road type
SELECT
  rs.road_type,
  ROUND(
    100.0 * SUM(
      CASE
        WHEN road_condition IN ('WET', 'ICE', 'SNOW', 'SLUSH', 'MOIST')
        THEN 1 ELSE 0
      END
    ) / COUNT(*),
    2
  ) AS bad_cond_percentage,
  ROUND(
    100.0 * SUM(
      CASE
        WHEN road_condition IN ('WET', 'ICE', 'SNOW', 'SLUSH', 'MOIST')
        THEN 0 ELSE 1
      END
    ) / COUNT(*),
    2
  ) AS good_cond_percentage


FROM 
  road_forecasts rf
  JOIN road_sections rs
  ON rf.section_id = rs.section_id
  GROUP BY road_type;


-- avg temperatures for all road condition types where tempreature of air is higher than road temperature and vice versa
SELECT rf.road_condition, 
AVG (CASE WHEN rf.air_temperature > rf.road_temperature THEN rf.road_temperature END) as avgtempairhigher, 
AVG (CASE WHEN rf.air_temperature < rf.road_temperature THEN rf.road_temperature END) as avgtempairlower 
FROM road_forecasts as rf
JOIN road_sections as rs on rf.section_id = rs.section_id 
GROUP BY rf.road_condition;