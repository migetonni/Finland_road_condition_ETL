from sqlalchemy import text





def load_etl_metadata(engine,run_id,
                      flow_name,
                      started_at,
                      finished_at,
                      status,
                      duration_seconds,
                      error_message):
    


    
    with engine.begin() as conn:
        conn.execute(text("""INSERT INTO etl_runs (run_id,
                                                flow_name,
                                                started_at,
                                                finished_at,
                                                status,
                                                duration_seconds,
                                                error_message)
                                                VALUES(:run_id,
                                                :flow_name,
                                                :started_at,
                                                :finished_at,
                                                :status,
                                                :duration_seconds,
                                                :error_message)"""),

                                            {
                                            "run_id": run_id,
                                            "flow_name": flow_name,
                                            "started_at": started_at,
                                            "finished_at": finished_at,
                                            "status": status,
                                            "duration_seconds": duration_seconds,
                                            "error_message": error_message,
                                        },
                                    )
    
    