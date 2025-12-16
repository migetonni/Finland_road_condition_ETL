**Finland Road Condition ETL Pipeline**

An automated ETL (Extract, Transform, Load) pipeline that fetches real-time road condition data from the FINtraffic API, processes it into a clean and usable format, and loads it into Supabase for storage and further analysis.

This pipeline is fully orchestrated and scheduled with Prefect Cloud, enabling reliable, maintainable, and automated data updates.

Features

- Automated Data Collection — Periodically extracts up-to-date road condition data from the FINtraffic API.

- Data Transformation — Cleans and structures the raw JSON data using pandas for easy downstream analysis.

- Cloud-Native Loading — Loads the processed data into a Supabase PostgreSQL database.

- Orchestration & Monitoring — Managed and scheduled with Prefect Cloud for observability, retry logic, and failure alerts.

  **TECH STACK**

| Tool              | Purpose                                            |
| ----------------- | -------------------------------------------------- |
| **Prefect Cloud** | Workflow orchestration, scheduling, and monitoring |
| **Supabase**      | Cloud Postgres database for data storage           |
| **pandas**        | Data wrangling and transformation                  |
| **SQLAlchemy**    | Database connection management                     |


**DEPLOYMENT**
This pipeline is deployed and managed via Prefect Cloud using the uv build system.
Example deployment command:
uvx prefect-cloud deploy flows/etl_pipeline.py:main \
  --from migetonni/Finland_road_condition_ETL \
  --name finroadETL \
  --with pandas \
  --with sqlalchemy \
  --with python-dotenv \
  --with supabase \
  --with psycopg2-binary \

FOR AUTOMATED SCHEDULED RUNS FOR MY INTENDED PURPOSE
uvx prefect-cloud schedule "main/finroadETL" "0 7 * * *"
<img width="427" height="376" alt="image" src="https://github.com/user-attachments/assets/d45236d7-ae24-4d2d-8f59-4b088a943f34" />


**AUTHOR**
*Mixu Koski-Homi*




