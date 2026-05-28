AUDIT_DB ="pipeline"
AUDIT_TABLE   = "audit_log"

spark.sql(f"CREATE DATABASE IF NOT EXISTS {AUDIT_DB}")
#spark.sql(f"drop table   {AUDIT_DB}.{AUDIT_TABLE} ")

spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {AUDIT_DB}.{AUDIT_TABLE} (
            audit_id          BIGINT GENERATED ALWAYS AS IDENTITY ,       -- unique ID per log entry
            run_id            STRING,       -- groups all stages in ONE daily run
            stage             STRING,       -- BRONZE / SILVER / GOLD
            resource_type     STRING,       -- Patient / Encounter / Condition
            operation         STRING,       -- INGEST / VALIDATE / SCD2 / VIEW_REFRESH
            status            STRING,       -- STARTED / SUCCESS / FAILED / SKIPPED
            -- ── Load Counts ──────────────────────────────────
            before_run_source_count      LONG,         -- records read from source
            post_run_source_count LONG, 
            inserted_count    LONG,         -- new records inserted
            updated_count     LONG,         -- records updated (SCD2 expired + new)
            -- ── Timestamps ───────────────────────────────────
            started_at        TIMESTAMP,    -- when this stage started
            completed_at      TIMESTAMP,    -- when this stage finished
            load_date         DATE,         -- which daily batch date
            -- ── Error Info ───────────────────────────────────
            error_message     STRING,       -- null if successful
            -- ── Metadata ─────────────────────────────────────
            created_by        STRING        -- notebook or job name
        )
        USING DELTA
        PARTITIONED BY (load_date, stage)""")
