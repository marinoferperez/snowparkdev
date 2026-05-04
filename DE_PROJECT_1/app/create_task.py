from snowflake.core import Root
from snowflake.snowpark import Session
import snowflake.connector
from datetime import timedelta
from snowflake.core.task import Task, StoredProcedureCall
import procedures
from snowflake.core.task.dagv1 import DAG, DAGTask, DAGOperation, DAGTaskBranch, CreateMode
import os

# conn = snowflake.connector.connect()

conn = snowflake.connector.connect(
    user=os.environ.get('SNOWFLAKE_USER'),
    password=os.environ.get('SNOWFLAKE_PASSWORD'),
    account=os.environ.get("SNOWFLAKE_ACCOUNT"),
    warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE'),
    database=os.environ.get('SNOWFLAKE_DATABASE'),
    schema=os.environ.get('SNOWFLAKE_SCHEMA'),
    role=os.environ.get('SNOWFLAKE_ROLE'))

print("connection establisehd")
print(conn)

root = Root(conn)
print(root)

# my_task = Task("my_task", StoredProcedureCall(procedures.hello_procedure, stage_location="@dev_deployment"), warehouse="compute_wh", schedule=timedelta(hours=1))

# create dag

with DAG("dag_copy_emp", schedule=timedelta(days=1)) as dag:
    dag_task1 = DAGTask("copy_from_s3", StoredProcedureCall(procedures.copy_to_table_proc, packages=["snowflake-snowpark-python"], imports=["@dev_deployment/my_de_project_1/app.zip"], stage_location="@dev_deployment"), warehouse="compute_wh")
    
    dag_task2 = DAGTask("execute_sql_statements", StoredProcedureCall(procedures.execute_sql_statements, packages=["snowflake-snowpark-python"], imports=["@dev_deployment/my_de_project_1/app.zip"], stage_location="@dev_deployment"), warehouse="compute_wh")

    # dependencies
    
    dag_task1 >> dag_task2
    
    schema = root.databases["demo_db"].schemas['public']
    dag_op = DAGOperation(schema)
    dag_op.deploy(dag, CreateMode.or_replace)
    
    