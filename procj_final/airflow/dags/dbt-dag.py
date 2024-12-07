from datetime import datetime

try:
    from airflow.operators.empty import EmptyOperator
except:
    from airflow.operators.dummy import DummyOperator as EmptyOperator

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.edgemodifier import Label
from airflow.providers.dbt.cloud.hooks.dbt import DbtCloudHook
from airflow.providers.dbt.cloud.operators.dbt import (DbtCloudRunJobOperator,
                                                       DbtCloudGetJobRunArtifactOperator,
                                                       DbtCloudListJobsOperator
                                                       )
from airflow.providers.dbt.cloud.sensors.dbt import DbtCloudJobRunSensor
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.python import PythonOperator

SNOW_FLAKE_CONN_ID = 'jg-airflow-snowflake-conn'
DBT_ACCOUNT_ID = 193671
DBT_CONN_ID = 'jg-airflow-dbt-conn'

def stage_snowflake():
    SHook = SnowflakeHook(snowflake_conn_id=SNOW_FLAKE_CONN_ID)
    conn = SHook.get_conn()
    cursor = conn.cursor()
    cursor.execute(rf"PUT file:///tmp/Founders.csv @startups")
    cursor.execute(rf"PUT file:///tmp/Startups.csv @startups")
    cursor.close()
    conn.close()


with DAG (
    dag_id='first-dbt-cloud-dag',
    start_date=datetime(2023, 8, 23),
    schedule='@once',
    catchup=False,
    default_args={"dbt_cloud_conn_id": DBT_CONN_ID,
                  "account_id": DBT_ACCOUNT_ID}
) as dag:
    begin = EmptyOperator(task_id="begin")
    end = EmptyOperator(task_id="end")

    download_startups_file = BashOperator(
        task_id = "download_startups_file",
        bash_command = "curl -o /tmp/Startups.csv https://storage.googleapis.com/kagglesdsdata/datasets/3626740/6304203/Startups.csv"
    )

    download_founders_file = BashOperator(
        task_id = "download_founders_file",
        bash_command = "curl -o /tmp/Founders.csv https://storage.googleapis.com/kagglesdsdata/datasets/3626740/6304203/Founders.csv"
    )

    list_files = BashOperator(
        task_id = "list_file",
        bash_command = "ls /tmp"
    )
    
    load_to_snowflake_internal_stage = PythonOperator(
        task_id = 'load_to_snowflake_internal_stage',
        python_callable = stage_snowflake
    )

    load_raw_staged_snowflake_data = SnowflakeOperator(
        task_id = 'load_raw_staged_snowflake_data',
        sql = 'load_staged_raw_data.sql',
        snowflake_conn_id = SNOW_FLAKE_CONN_ID
    )


    trigger_job_run1 = DbtCloudRunJobOperator(
        task_id="trigger_job_run1",
        job_id=407207,
        check_interval=10,
        timeout=300
    )

    get_run_results_artifact = DbtCloudGetJobRunArtifactOperator(
        task_id="get_run_results_artifact", 
        run_id=trigger_job_run1.output, 
        path="run_results.json"
    )

    job_run_sensor = DbtCloudJobRunSensor(
        task_id="job_run_sensor", 
        run_id=trigger_job_run1.output, 
        timeout=20
    )
    
    list_dbt_jobs = DbtCloudListJobsOperator(
        task_id = 'list_dbt_jobs',
        project_id=282705
    )

    begin >> [download_startups_file, download_founders_file] >> list_files >> load_to_snowflake_internal_stage >> load_raw_staged_snowflake_data >> Label('Wait with sensor') >> trigger_job_run1
    [get_run_results_artifact, job_run_sensor, list_dbt_jobs] >> end
