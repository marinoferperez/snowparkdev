import sys
import os
import yaml

# os.system(f"conda init")
# os.system(f"conda activate snowpark")
directory_path= sys.argv[1]


os.chdir(f"{directory_path}")
# Make sure all 6 SNOWFLAKE_ environment variables are set
# SnowCLI accesses the passowrd directly from the SNOWFLAKE_PASSWORD environmnet variable
os.system(f"snow snowpark build")
os.system(f"snow snowpark deploy --replace --temporary-connection --account $SNOWFLAKE_ACCOUNT_DEV --user $SNOWFLAKE_USER_DEV --role $SNOWFLAKE_ROLE_DEV --warehouse $SNOWFLAKE_WAREHOUSE_DEV --database $SNOWFLAKE_DATABASE_DEV")  