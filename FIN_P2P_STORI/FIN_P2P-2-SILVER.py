"""
### FIN Procurement to Pay --> P2P
#### SUMMARY:
--------
#### DAG Name:
    FIN_P2P_SILVER.py
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
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import Variable
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.task_group import TaskGroup
from airflow.models.baseoperator import chain


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
    silver_tasks,
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
queries_base_path = os.path.join(os.path.dirname(__file__), "queries/2-SILVER/")

# # # -----------------------dag definition------------------------------
with DAG(
    "FIN_P2P_SILVER",
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
        trigger_rule="all_success"
    )
    with TaskGroup("FINISH_TASK_GROUP") as FINISH_TASK:
        TRIGGER_DAG_GOLD = TriggerDagRunOperator(
            task_id="TRIGGER_DAG_GOLD",
            trigger_dag_id="FIN_P2P_GOLD",
            trigger_rule="all_success"
        )
    TRANSACTIONS = MultiStatementSnowflakeOperator(
        task_id="TRANSACTIONS",
        sql="P2P_TRANSACTIONS.sql",
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
    for task in silver_tasks:
        SILVER_LOW_LEVEL_TASK = MultiStatementSnowflakeOperator(
            task_id=f"{task}_LOW_LEVEL_SILVER_TASK",
            sql=f"1-LOW_LEVEL/P2P_{task}.sql",
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
        SILVER_DOMAIN_TASK = MultiStatementSnowflakeOperator(
            task_id=f"{task}_DOMAIN_SILVER_TASK",
            sql=f"2-DOMAIN/P2P_{task}.sql",
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
            >> SILVER_LOW_LEVEL_TASK
            >> SILVER_DOMAIN_TASK
            >> TRANSACTIONS
            >> FINISH_TASK
            >> END_DAG
        )