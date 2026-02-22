
## Architecture Overview

Sensors (Raspberry Pi)
        ↓
    AWS S3 (raw CSV files)
        ↓
 ETL Script (Python)
        ↓
 PostgreSQL Database
        ↓
 Web / Dashboard (future)

## Project Structure
data-transferring/
├── etl_s3_to_postgres.py    # ETL script (S3 → PostgreSQL)
├── requirements.txt         # Python dependencies
├── .gitignore               # Ignored files (venv, .env, etc.)
├── sql/
│   └── schema.sql           # Database schema
└── README.md

## Requirements
- Python 3.10 or higher
- PostgreSQL 14 or higher
- AWS account with access to S3
- pgAdmin4

## Python Dependencies

pip install -r requirements.txt

Main libraries used:
- `boto3` – AWS S3 access
- `pandas` – data processing and cleaning
- `psycopg2-binary` – PostgreSQL connection
- `python-dotenv` – environment variable management

## Database Setup
1. Open pgAdmin
2. Create a PostgreSQL database (e.g. sensor_data)
3. Open the Query Tool
4. Run the schema file located at: sql/schema.sql

# Enviroment Variables

Create a .env file and paste the following values:
DB_HOST=localhost
DB_NAME=sensor_data
DB_USER=postgres
DB_PASSWORD=your_postgres_password
