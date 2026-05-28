fhir-lakehouse/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── config/
│   ├── __init__.py
│   └── config.py
│
├── utils/
│   ├── __init__.py
│   └── fhir_utils.py
│
├── notebooks/
│   ├── 00_setup.py
│   ├── 01_raw_ingestion.py
│   ├── 02_bronze_layer.py
│   ├── 03_silver_layer.py
│   ├── 04_gold_layer.py
│   └── 05_scd2_versioning.py
│
├── pipelines/
│   └── orchestration_pipeline.json
│

