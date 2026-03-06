# ETL Sales Pipeline — Jenkins CI/CD

A dirty CSV goes in, a clean Parquet comes out. Jenkins makes sure nothing breaks along the way.

## What this is

A Python ETL pipeline wrapped in a Jenkins CI/CD setup. Built to learn how CI/CD works in a data engineering context — not a web app tutorial with Express.js.

The pipeline reads messy sales data (nulls, negative quantities, inconsistent dates, mixed-case statuses), cleans it, and outputs Parquet. Jenkins automates the whole chain: lint the code, run tests, build a Docker image, and deploy.

## The pipeline

```
sales_raw.csv → [extract] → [transform] → [load] → sales_clean.parquet
```

**What gets cleaned:**
- Rows with missing customer, product, or region → dropped
- Zero or negative quantities → removed
- Mixed date formats (`2025-01-15` vs `01/22/2025`) → standardized
- Status casing (`COMPLETED`, ` pending `) → normalized

## Jenkins stages

```
Install → Lint → Test → Build Docker Image → Deploy
```

Any stage fails, the pipeline stops. No bad code reaches production.

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest test_pipeline.py -v
python pipeline.py
```

## Built with

Python, pandas, pytest, flake8, Docker, Jenkins

## What I learned

Jenkins doesn't touch your data — it guards your code. Airflow orchestrates data, Jenkins orchestrates deployments. A "build" is just one run of the pipeline. Linting is spell-check for code. And the first Jenkins build always fails.
