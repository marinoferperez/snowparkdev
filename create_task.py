from snowflake.core import Root
import snowflake.connector
from datetime import timedelta
from snowflake.core.task import Task, StoredProcedureCall
from first_snowpark_project.app import procedures
from snowflake.core.task.dagv1 import DAG, DAGTask, DAGOperation, CreateMode

conn = snowflake.connector.connect()
print("connection establisehd")
print(conn)

root = Root(conn)
print(root)

my_task = Task("my_task", StoredProcedureCall(procedures.hello_procedure, stage_location="@dev_deployment"), warehouse="compute_wh", schedule=timedelta(hours=1))

tasks = root.databases["demo_db"].schemas['public'].tasks

tasks.create(my_task, mode=CreateMode.or_replace)

# create dag

with DAG("my_dag", schedule=timedelta(days=1)) as dag:
    dag_task1 = DAGTask("my_hello_task", StoredProcedureCall(procedures.hello_procedure, args=["mafperez"], packages=["snowflake-snowpark-python"], imports=["@dev_deployment/my_snowpark_project/app.zip"], stage_location="@dev_deployment"), warehouse="compute_wh")

    dag_task2 = DAGTask("my_test_task", StoredProcedureCall(procedures.test_procedure, packages=["snowflake-snowpark-python"], imports=["@dev_deployment/my_snowpark_project/app.zip"], stage_location="@dev_deployment"), warehouse="compute_wh")
    
    # dependencies
    
    dag_task1 >> dag_task2
    
    schema = root.databases["demo_db"].schemas['public']
    dag_op = DAGOperation(schema)
    dag_op.deploy(dag, CreateMode.or_replace)