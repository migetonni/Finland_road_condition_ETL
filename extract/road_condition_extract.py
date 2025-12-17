import requests
import pandas as pd
import json


def get_road_weather_data():

    results = requests.get("https://tie.digitraffic.fi/api/weather/v1/forecast-sections/forecasts", timeout=10)
    results.raise_for_status()
    data = results.json()
    
    return data
    


    
def get_road_data():
    results = requests.get("https://tie.digitraffic.fi/api/weather/v1/forecast-sections",timeout=10)
    results.raise_for_status()
    data = results.json()
        
    return data
        


def load_street_forecast():

    road_data = get_road_data()
    road_weather_data = get_road_weather_data()

    road_sections_data = []
    forecast_data = []

    for section in road_data["features"]:
        section_id = section["id"]
        section_coordinates = section["geometry"]["coordinates"]

        for i in road_weather_data["forecastSections"]:
            if i["id"] == section_id:
                 condition_list = i["forecasts"]
                 for forecast in condition_list:
                    road_sections_data.append({
                    "section_id": section_id,
                    "coordinates": section_coordinates})
                    forecast_data.append({
                    "section_id": section_id,
                    "forecast_time": forecast.get("time"),
                    "forecast_type": forecast.get("type"),
                    "forecast_name": forecast.get("forecastName"),
                    "daylight": forecast.get("daylight"),
                    "road_temperature": forecast.get("roadTemperature"),
                    "air_temperature": forecast.get("temperature"),
                    "wind_speed": forecast.get("windSpeed"),
                    "wind_direction": forecast.get("windDirection"),
                    "overall_road_condition": forecast.get("overallRoadCondition"),
                    "weather_symbol": forecast.get("weatherSymbol"),
                    "reliability": forecast.get("reliability"),
                    "data_updated_time": forecast.get("dataUpdatedTime"),
                    # Optional fields that might not always be present 
                    "precipitation_condition": forecast.get("forecastConditionReason", {}).get("precipitationCondition"),
                    "road_condition": forecast.get("forecastConditionReason", {}).get("roadCondition")
                })
    road_df = pd.DataFrame.from_dict(road_sections_data)
    forecast_df = pd.DataFrame.from_dict(forecast_data)

    return road_df, forecast_df

                    
if __name__ == "__main__":
    df = load_street_forecast()
    print(df["forecast_name"])





