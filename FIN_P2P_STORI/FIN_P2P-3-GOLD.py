"""
### FIN Procurement to Pay --> P2P
#### SUMMARY:
--------
#### DAG Name:
    FIN_P2P_GOLD.py
#### Owner:
    dcamilovelez0126@gmail.com
#### Leader:
    camilo.baquero@storicard.com
#### Description:
    This DAG generates the data model for Procurement to Pay infrastructure in Gold Layer,
    using data from External sources + Manual Inputs to be send through API to Netsuite.
#### Output:
    TBD.
"""

# Native Imports
import os
from datetime import datetime
from settings import set_variable
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.task_group import TaskGroup


# Internal Imports
from rappiflow.operators import MultiStatementSnowflakeOperator
from dags.utils.powerbi_api import set_refresh_dataset

# Auxiliar Imports
from dags.verticals.Finances.Datamarts.Global_finances.FIN_P2P.FIN_P2P_AUX import (
    settings,
    var_schema,
    var_db_silver,
    var_db_gold,
    default_args,
    gold_tasks,
    gold_dataset_transactions,
)

# # # -----------------------Envoironment Variables Definition------------------------------
vars_name = "FIN_P2P"
vars_value = {
    "REQUISITIONS": "",
    "PURCHASE_ORDERS": "",
    "CONTRACTS": "",
    "INVOICE": "",
    "USERS": "",
    "SUPPLIERS": "",
    "DEFAULT": ""
}
vars_dag = Variable.get(vars_name, default_var={}, deserialize_json=True)

# # # -----------------------Others Vars Definition------------------------------
queries_base_path = os.path.join(os.path.dirname(__file__), "queries/3-GOLD/")

# # # -----------------------dag definition------------------------------

with DAG(
    "FIN_P2P_GOLD",
    max_active_runs=1,
    schedule=None,
    start_date=datetime(2020, 1, 14),
    default_args=default_args,
    concurrency=3,
    catchup=False,
    template_searchpath=queries_base_path,
    tags=["SchedulerMonitoring", "P1", "Tier1", "FIN_P2P", "FIN"],
    doc_md=__doc__,
) as dag:

    START_DAG = DummyOperator(
        task_id="START_DAG",
        trigger_rule="all_success"
    )
    END_DAG = DummyOperator(
        task_id="END_DAG",
        trigger_rule="all_done"
    )
    with TaskGroup("FINISH_TASK_GROUP") as FINISH_TASK:
        SET_VARIABLES = PythonOperator(
            task_id='SET_DEFAULT_VARIABLES',
            provide_context=True,
            dag=dag,
            op_kwargs={
                "variable_name": vars_name,
                "variable_value": vars_value
            },
            python_callable=set_variable
        )
        TRIGGER_DAG_TO_NETSUITE = TriggerDagRunOperator(
            task_id="TRIGGER_DAG_TO_NETSUITE",
            trigger_dag_id="FIN_P2P-4-TO_NETSUITE",
            wait_for_completion=True,
            trigger_rule="all_success"
        )
        REFRESH_DASH_TRANSACTIONS = PythonOperator(
            task_id="REFRESH_DASH_TRANSACTIONS",
            provide_context=True,
            python_callable=set_refresh_dataset,
            op_kwargs={"datasets": gold_dataset_transactions},
            trigger_rule="all_done",
        )
    for task in gold_tasks:
        if task == 'TRANSACTIONS':
            sql_file = f"P2P_{task}.sql"
        else:
            sql_file = f"{task}/P2P_{task}.sql"
        GOLD_TASK = MultiStatementSnowflakeOperator(
            task_id=f"{task}_GOLD_TASK",
            sql=sql_file,
            snowflake_conn_id=settings["snowflake_conn_id"],
            params={
                "db_gold": var_db_gold,
                "db_silver": var_db_silver,
                "schema": var_schema,
            },
            default_args=default_args,
            retries=0,
            trigger_rule="all_success",
        )
        if task in ("VENDORBILL","VENDORCREDIT"):
            LINE_TASK = MultiStatementSnowflakeOperator(
                task_id=f"{task}_LINE_GOLD_TASK",
                sql=f"{task}/P2P_{task}_LINE.sql",
                snowflake_conn_id=settings["snowflake_conn_id"],
                params={
                    "db_gold": var_db_gold,
                    "db_silver": var_db_silver,
                    "schema": var_schema,
                },
                default_args=default_args,
                retries=0,
                trigger_rule="all_success",
            )
            (
                START_DAG
                >> LINE_TASK
                >> GOLD_TASK
            )
        (
            START_DAG
            >> GOLD_TASK
            >> FINISH_TASK
            >> END_DAG
        )
