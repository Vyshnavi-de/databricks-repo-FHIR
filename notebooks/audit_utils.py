from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp
from datetime import datetime
import uuid

spark = SparkSession.builder.getOrCreate()

def audit_start(
    run_id: str,
    stage: str,          
    resource_type: str,  
    operation: str,      
    status: str,         
    started_at: datetime,
    before_run_source_count: int = 0,
    inserted_count: int = 0,
    updated_count: int = 0,
    pipeline_name: str = "FHIR_Daily_Load",
    created_by: str = "pipeline",
):

    now = datetime.utcnow()
    started_at = started_at or now

    started_at_str = started_at.strftime("%Y-%m-%d %H:%M:%S")
    load_date_str = str(now.date())
    
    spark.sql(f"""
        INSERT INTO pipeline.audit_log (
            run_id, stage, resource_type, operation, status,
            before_run_source_count, post_run_source_count, inserted_count, updated_count,
            started_at, completed_at, load_date,
            error_message, created_by
        )
        VALUES (
            '{run_id}', '{stage.upper()}', '{resource_type}', '{operation.upper()}', '{status.upper()}',
            {before_run_source_count}, 0, {inserted_count}, {updated_count},
            '{started_at_str}', NULL, '{load_date_str}', '',  '{created_by}'
        )
    """)

def audit_end(
    run_id: str,
    stage: str,
    resource_type: str,
    operation: str,
    status: str,                      # "SUCCESS" / "FAILED" / "SKIPPED"
    post_run_source_count: int = 0,
    inserted_count: int = 0,
    updated_count: int = 0,
    error_message: str = ""
):
    now = datetime.utcnow()

    completed_at_str = now.strftime("%Y-%m-%d %H:%M:%S")

    spark.sql(f"""update pipeline.audit_log set status ='{status}', post_run_source_count = {post_run_source_count} , inserted_count={inserted_count}, updated_count={updated_count} , completed_at ='{completed_at_str}' , error_message ='{error_message}'  where run_id='{run_id}' and resource_type='{resource_type}'""")
    print(
        f" {resource_type} | {operation} | {status} | "
        f"Post_run_src_count = {post_run_source_count} , updated_count = {updated_count} , inserted_count = {inserted_count}")
    
  

