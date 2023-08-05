from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pipeline.data_ingestion import DataIngestion
from pipeline.feature_engineering import FeatureEngineering
from pipeline.train import Train
from pipeline.simulation import Simulation
import pandas as pd
import numpy as np
from configuration import *

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['aameerhamza1801@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'currency_forecast_dag',
    default_args=default_args,
    start_date=datetime(2023, 8, 4),
    description='A DAG to forecast currency using ML',
    schedule=timedelta(days=1),
)

def run_data_ingestion():
    di = DataIngestion(data_loc.split('/')[-1].split('.')[0])
    data = di.get_data(data_loc)
    return data.to_json(date_format='iso')

def run_feature_engineering(**context):
    ti = context['task_instance']
    data_json = ti.xcom_pull(task_ids='data_ingestion_task')
    data = pd.read_json(data_json)
    fe = FeatureEngineering(data)
    train_x, train_y, range_ = fe.create_features(feature_window)
    return {'train_x': train_x.tolist(), 'train_y': train_y.tolist(), 'range_': range_}

def run_train_model(**context):
    ti = context['task_instance']
    train_data = ti.xcom_pull(task_ids='feature_engineering_task')
    train_x = np.array(train_data['train_x'])
    train_y = np.array(train_data['train_y'])
    trainer = Train(train_x, train_y)
    trainer.train(accuracy_location, model_location)

def run_simulation(**context):
    ti = context['task_instance']
    test_data = ti.xcom_pull(task_ids='feature_engineering_task')
    range_ = np.array(test_data['range_'])
    data_x = np.array(test_data['train_x'])
    data_y = np.array(test_data['train_y'])
    simulator = Simulation(data_x, data_y, 0.95)
    simulator.simulate(model_location, simulation_location, range_)

data_ingestion_task = PythonOperator(
    task_id='data_ingestion_task',
    python_callable=run_data_ingestion,
    dag=dag
)

feature_engineering_task = PythonOperator(
    task_id='feature_engineering_task',
    python_callable=run_feature_engineering,
    dag=dag
)

train_model_task = PythonOperator(
    task_id='train_model_task',
    python_callable=run_train_model,
    dag=dag
)

simulate_model_task = PythonOperator(
    task_id='simulate_model_task',
    python_callable=run_simulation,
    dag=dag
)

data_ingestion_task >> feature_engineering_task >> train_model_task >> simulate_model_task