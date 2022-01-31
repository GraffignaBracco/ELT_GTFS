from datetime import timedelta
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from gtfs_elt.functions import extract_gtfs, load_gtfs
        

def _extract_gtfs(endpoint, ti):
    path = extract_gtfs(endpoint)

    ti.xcom_push(key='last_gtfs_path', value=path)

def _load_gtfs(ti):
    path =  ti.xcom_pull(key='last_gtfs_path', task_ids='extract_vehiclePositions')
    load_gtfs(path)


default_args = {
    'owner': 'juan',
    'retries': 0,
}

with DAG("extract_load_vehpo",default_args=default_args, catchup=False, schedule_interval=timedelta(minutes=1), start_date=datetime(2022, 1, 18, 21, 40, 0)) as dag:
    

    extract_vehiclePositions =  PythonOperator(

        task_id="extract_vehiclePositions",
        python_callable=_extract_gtfs,
        op_args=['vehiclePositions']
    )
     
    load_vehiclePositions =  PythonOperator(

        task_id="load_vehiclePositions",
        python_callable=_load_gtfs,
    )
    extract_vehiclePositions >> load_vehiclePositions
