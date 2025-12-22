## Finland Road Condition ETL Pipeline

An automated ETL (Extract, Transform, Load) pipeline that fetches real-time road condition data from the FINtraffic API, processes it into a clean and analytics-ready format, and loads it into Supabase for storage and further analysis and visualization.

This pipeline is fully orchestrated and scheduled with Prefect Cloud, enabling reliable, maintainable, and automated data updates.

Features

- Automated Data Collection From the FinTraffic APIs

- Data Transformation using Pandas

- Cloud-Native Loading to Supabase
  
- Orchestration & Monitoring using Prefect cloud

- Historical fact storage

- ETL run metadata and observability

- Analytics views for BI tools (Power BI)



  **TECH STACK**

  

| Tool              | Purpose                                            |
| ----------------- | -------------------------------------------------- |
| **Prefect Cloud** | Workflow orchestration, scheduling, and monitoring |
| **Supabase**      | Cloud Postgres database for data storage           |
| **pandas**        | Data wrangling and transformation                  |
| **SQLAlchemy**    | Database connection management                     |

**Database Design**


## Database Design

The database schema follows analytics best practices by separating:

### Core Tables
- `road_sections` static road metadata
- `road_forecasts`  latest snapshot of road conditions
- `historical_road_conditions`  immutable historical fact table

### Domain (Lookup) Tables
- `precipitation_types`
- `road_condition_types`
- `overall_road_condition_types`
- `reliability_types`

Domain tables are loaded idempotently to avoid duplication and ensure data consistency.

### ETL Metadata
- `etl_runs` — captures execution status, duration, and errors for each pipeline run


<img width="771" height="652" alt="image" src="https://github.com/user-attachments/assets/67ad4a6c-e7a8-46b3-8149-08d876176b31" />





**DEPLOYMENT**


This pipeline is deployed and managed via Prefect Cloud using the uv build system.
Example deployment command:

```
uvx prefect-cloud deploy flows/etl_pipeline.py:main \
  --from migetonni/Finland_road_condition_ETL \
  --name finroadETL \
  --with pandas \
  --with sqlalchemy \
  --with python-dotenv \
  --with supabase \
  --with psycopg2-binary \
```

FOR AUTOMATED SCHEDULED RUNS FOR MY INTENDED PURPOSE

```
uvx prefect-cloud schedule "main/finroadETL" "0 7 * * *"
```

<img width="427" height="376" alt="image" src="https://github.com/user-attachments/assets/d45236d7-ae24-4d2d-8f59-4b088a943f34" />


**ANALYTICS**


The data produced from this ETL pipeline can be used for many types of analysis and dashboard creations of road conditions.
From the example_queries.sql file you can find some queries that provide descriptive analytics from the data.

The pipeline exposes analytics-ready data via a SQL view:

- `powerbi_road_conditions`

Below is an example dashboard created in PowerBI from the the produced road data that utilizes the analytics view that is created in SQL

<img width="1297" height="730" alt="image" src="https://github.com/user-attachments/assets/6818eb51-5da4-43b1-8d2d-4b705417f6c3" />



**AUTHOR**


*Mixu Koski-Homi*




