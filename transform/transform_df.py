import pandas as pd
import json

def transform_track_df(df):

    #copy dataframe
    df = df.copy()

    #dropping duplicates

    df = df.drop_duplicates(subset=["section_id", "forecast_time"], keep="last")

    #transforming the contents of the coordinates columns to json  string so no index of different sizes errors in the load phase
    if "coordinates" in df.columns:
        df["coords_json"] =df["coordinates"].apply(lambda x: json.dumps(x))

        df = df.drop(columns=["coordinates"])

    #drop rows with old information since we only want the latest road condition data
    forecast_times = ['0h', '2h', '4h', '6h']

    df = df[df["forecast_name"].isin(forecast_times)]

    df["road_number"] = (
            df["section_id"]
            .str.split("_")
            .str[0]
            .astype("Int64")
        )
    

    def road_classifier(num):
        if pd.isna(num):
            return "unknown"
        if num < 40:
            return "mainRoad"
        elif num > 39 and num < 100:
            
            return "secondaryRoad"
        else:
            return "minorRoad"
        
    df["road_type"] = df["road_number"].apply(road_classifier)

    
    
    

    return df
    





    
