import requests
import pandas as pd
import json


def get_road_weater_data():

    results = requests.get("https://tie.digitraffic.fi/api/weather/v1/forecast-sections/forecasts")

    if results.status_code == 200:
        data = results.json()
    
        return data
    
    else:
        return None
    
def get_road_data():
    results = requests.get("https://tie.digitraffic.fi/api/weather/v1/forecast-sections")
    if results.status_code == 200:
        data = results.json()
        
        return data
        
    else:
        return None


def load_street_forecast():

    road_data = get_road_data()
    road_weather_data = get_road_weater_data()

    joined_data = []

    for section in road_data["features"]:
        section_id = section["id"]
        section_coordinates = section["geometry"]["coordinates"]

        for i in road_weather_data["forecastSections"]:
            if i["id"] == section_id:
                 condition_list = i["forecasts"]
                 for forecast in condition_list:
                    joined_data.append({
                    "section_id": section_id,
                    "coordinates": section_coordinates,
                    "forecast_time": forecast["time"],
                    "forecast_type": forecast["type"],
                    "forecast_name": forecast["forecastName"],
                    "daylight": forecast["daylight"],
                    "road_temperature": forecast["roadTemperature"],
                    "air_temperature": forecast["temperature"],
                    "wind_speed": forecast["windSpeed"],
                    "wind_direction": forecast["windDirection"],
                    "overall_road_condition": forecast["overallRoadCondition"],
                    "weather_symbol": forecast["weatherSymbol"],
                    "reliability": forecast["reliability"],
                    "data_updated_time": forecast["dataUpdatedTime"],
                    # Optional fields that might not always be present 
                    "precipitation_condition": forecast.get("forecastConditionReason", {}).get("precipitationCondition"),
                    "road_condition": forecast.get("forecastConditionReason", {}).get("roadCondition")
                })
    df = pd.DataFrame.from_dict(joined_data)
    return df

                    

df = load_street_forecast()
print(df)





