# ETL Sales Pipeline: Jenkins CI/CD

A dirty CSV goes in, a clean Parquet comes out. Jenkins makes sure nothing breaks along the way.

## What this is

A Python ETL pipeline wrapped in a Jenkins CI/CD setup. Here, I Built to learn how CI/CD works in a data engineering context. 

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

A product team needs dashboards. Data engineers write extract scripts that pull from APIs and databases, load raw data into S3, and dbt models transform it from bronze to silver to gold. All of that code and the extract scripts, the dbt models, the Airflow DAGs lives in a repo. CI/CD is the layer that sits between your code and production. When someone on the team pushes a change to a dbt model, Jenkins (or GitHub Actions) pulls that code, lints it, runs tests, builds the Docker image, and only then deploys it to wherever Airflow or dbt Cloud will pick it up. If a teammate accidentally writes a transform that drops valid rows, CI/CD catches it before it ever touches the warehouse and ruins someone's dashboard.
