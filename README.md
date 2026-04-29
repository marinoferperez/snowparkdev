# snowparkdev

## Snowpark runtime in one place

This repo includes a small generator so you do not have to edit runtime for each function/procedure manually.

- Template: `first_snowpark_project/snowflake.template.yml`
- Generator: `first_snowpark_project/generate_snowflake_yml.py`
- Output used by deploy: `first_snowpark_project/snowflake.yml`

Run from `first_snowpark_project`:

```bash
python generate_snowflake_yml.py
```

Or choose a runtime once and apply it to all entries:

```bash
PY_RUNTIME=3.11 python generate_snowflake_yml.py
```