from airflow.models import Variable
from settings import get_default_args_opsgenie


# ---- General definitions
settings = {
    "snowflake_conn_id": "fincor_deb_su_connection",
    "google_sheets_id": "conn_google_sheets",
}

ENV = Variable.get("ENV", "")

if ENV == "FIVETRAN":
    var_db_silver = "STORI_SILVER_DB_PROD"
    var_db_gold = "STORI_GOLD_DB_PROD"
else:
    var_db_silver = "STORI_SILVER_DB_DEV"
    var_db_gold = "STORI_GOLD_DB_DEV"

var_schema = 'P2P'

url_notifications = "T2QSQ3L48/7374059876580/5706198f32e597f5f1f005c7b236abbb"

default_args = get_default_args_opsgenie(
    "FIN", url_notifications, "P1", "dcamilovelez0126@gmail.com"
)

# ---- Gold definitions
gold_dataset_transactions = ["41e9e850-42eb-47c5-a247-b9a6f5918af4"]

gold_tasks = [
    'TRANSACTIONS',
    'VENDORBILL',
    'VENDORCREDIT'
]

# ---- Silver definitions
silver_tasks = [
    'INVOICES',
    'PURCHASE_ORDERS',
    'MANUAL_INPUTS'
]
