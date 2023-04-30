from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.airbyte.operators.airbyte import AirbyteTriggerSyncOperator
from dotenv import load_dotenv
from datetime import timedelta
import json
import os

load_dotenv()

demographics_conn_id = os.environ.get("DEMOGRAPHICS_CONN_ID")
economy_conn_id = os.environ.get("ECONOMY_CONN_ID")
epidemiology_conn_id = os.environ.get(" EPIDEMIOLOGY_CONN_ID")
index_conn_id = os.environ.get("INDEX_CONN_ID")

default_args = {'owner' : 'gabriel',
                'retries' : 2,
                'retry_delay' : timedelta(minutes = 2)
                }

with DAG(

    dag_id = 'trigger_airbyte_dbt_job',
    schedule_interval = "@daily",
    start_date = days_ago(1),
    catchup = False,
    default_args = default_args

) as dag:

    airbyte_demographics_sync = AirbyteTriggerSyncOperator(

        task_id = 'demographics_sync',
        connection_id = demographics_conn_id,
        asynchronous = False,
        timeout = 36000

    )

    airbyte_economy_sync = AirbyteTriggerSyncOperator(

        task_id = 'economy_sync',
        connection_id = economy_conn_id,
        asynchronous = False,
        timeout = 36000

    )

    airbyte_index_sync = AirbyteTriggerSyncOperator(

        task_id = 'index_sync',
        connection_id = index_conn_id,
        asynchronous = False,
        timeout = 36000
    )

    airbyte_epidemiology_sync = AirbyteTriggerSyncOperator(

        task_id = 'epidemiology_sync',
        connection_id = epidemiology_conn_id,
        asynchronous = False,
        timeout = 36000

    )

airbyte_demographics_sync >> airbyte_economy_sync >> airbyte_index_sync >> airbyte_epidemiology_sync