import pandas as pd
import json

def transform_track_df(df):
    #dropping duplicates

    df = df.drop_duplicates(subset=["section_id", "forecast_time"], keep="last")

    #transforming the contents of the coordinates columns to json  string so no index of different sizes errors in the load phase
    if "coordinates" in df.columns:
        df["coords_json"] =df["coordinates"].apply(lambda x: json.dumps(x))

        df = df.drop("coordinates", axis= 1)

    #drop rows with old information since we only want the latest road condition data

    df = df.query("forecast_name == '2h' or forecast_name == '0h'")

    df["road_number"] = df["section_id"].str.split("_").str[0].astype(int)
    print(df["road_number"])

    def road_classifier(num):
        if num < 39:
            return "mainRoad"
        elif num > 39 and num < 100:
            
            return "secondaryRoad"
        else:
            return "minorRoad"
        
    df["road_type"] = df["road_number"].apply(road_classifier)

    
    
    

    return df
    





    
