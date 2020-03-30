from datetime import timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

import pandas as pd
from sqlalchemy import create_engine

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=20),
}

# Inicialización del grafo DAG de tareas para el flujo de trabajo

dag = DAG(
    'practica2',
    default_args=default_args,
    description='Grafo que define el trabajo de la práctica 2.',
    schedule_interval=timedelta(days=1),
)

# Prepamos el entorno

PrepararEntorno = BashOperator(
    task_id='PrepararEntorno',    
    depends_on_past=False,    
    bash_command='mkdir /tmp/workflow/',    
    dag=dag,
)

# Capturamos los datos

CapturaDatosA = BashOperator(
    task_id='CapturaDatosA',    
    depends_on_past=False,    
    bash_command='wget --output-document /tmp/workflow/humidity.csv.zip https://github.com/manuparra/MaterialCC2020/raw/master/humidity.csv.zip',    
    dag=dag,
)

CapturaDatosB = BashOperator(
    task_id='CapturaDatosB',    
    depends_on_past=False,    
    bash_command='curl -L -o /tmp/workflow/temperature.csv.zip https://github.com/manuparra/MaterialCC2020/raw/master/temperature.csv.zip',    
    dag=dag,
)

# Los desempaquetamos

DesempaquetaDatos = BashOperator(
    task_id='DesempaquetaDatos',    
    depends_on_past=False,    
    bash_command='unzip "/tmp/workflow/*.csv.zip" -d /tmp/workflow/',    
    dag=dag,
)

# Clonamos los datos del repositorio || git clone -b <BRANCH> <REPO>

CapturaCodigoFuenteV1 = BashOperator(
    task_id='CapturaCodigoFuenteV1',    
    depends_on_past=False,    
    bash_command='git clone -b service_V1 https://github.com/iMiguel10/airflow-CC.git /tmp/workflow/serviceV1',    
    dag=dag,
)

CapturaCodigoFuenteV2 = BashOperator(
    task_id='CapturaCodigoFuenteV2',    
    depends_on_past=False,    
    bash_command='git clone -b service_V2 https://github.com/iMiguel10/airflow-CC.git /tmp/workflow/serviceV2',    
    dag=dag,
)

# Levantamos la Base de datos

LevantaDB = BashOperator(
    task_id='LevantaDB',    
    depends_on_past=False,    
    bash_command='docker-compose -f ~/airflow/dags/docker-compose.yml up -d db',    
    dag=dag,
)

# Limpiamos y cargamos los datos en la base de datos

def limpiaYguardaDatos():

    # -------------- Limpiado de datos ------------------------------------ #
    
    df_temperature = pd.read_csv('/tmp/workflow/temperature.csv', header=0)
    df_humidity = pd.read_csv('/tmp/workflow/humidity.csv', header=0)
    
    df_temperature.rename(columns={'San Francisco':'Temperature'},inplace=True)
    df_humidity.rename(columns={'San Francisco':'Humidity'},inplace=True)
    
    df_temperature = df_temperature.loc[:, ['datetime','Temperature']]
    df_humidity = df_humidity.loc[:, ['datetime','Humidity']]
    
    merged = df_temperature.merge(df_humidity , on='datetime')
    
    merged["Temperature"] = merged["Temperature"].fillna(merged["Temperature"].mean())
    merged["Humidity"] = merged["Humidity"].fillna(merged["Humidity"].mean())
    
    # ------------- Guardar datos en la base de datos --------------------------------- #

    engine = create_engine('mysql+pymysql://miguel:miguel@localhost/forecast')
    merged.to_sql('forecast', con=engine, if_exists='replace')


LimpiayCargaDatos = PythonOperator(
    task_id='LimpiaCargaDatos',
    python_callable=limpiaYguardaDatos,
    dag=dag,
)

# Testeamos los servicios 

TestServicioV1 = BashOperator(
    task_id='TestServicioV1',    
    depends_on_past=False,    
    bash_command='export HOST=localhost && cd /tmp/workflow/serviceV1/test && pytest',    
    dag=dag,
)

TestServicioV2 = BashOperator(
    task_id='TestServicioV2',    
    depends_on_past=False,    
    bash_command='export API_KEY=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJpbWlndWVsMTBAY29ycmVvLnVnci5lcyIsImp0aSI6IjZkYjYwZjc4LWE4OTktNDJkYy1iZWNiLWJjNGIzNTJjNDAxNSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTg1MjM3NDI0LCJ1c2VySWQiOiI2ZGI2MGY3OC1hODk5LTQyZGMtYmVjYi1iYzRiMzUyYzQwMTUiLCJyb2xlIjoiIn0.eSfvLaehV_s3IdnpQ7fmMdNtYc8b3Kg28MKJHE6MN1o && cd /tmp/workflow/serviceV2/test && pytest',    
    dag=dag,
)

# Levantamos los servicios 

LevantaServicios = BashOperator(
    task_id='LevantaServicios',    
    depends_on_past=False,    
    bash_command='docker-compose -f ~/airflow/dags/docker-compose.yml up -d',    
    dag=dag,
)

# TAREAS 

# PrepararEntorno
# CapturaCodigoFuenteV1
# CapturaCodigoFuenteV2
# CapturaDatosA
# CapturaDatosB
# DesempaquetaDatos
# LevantaDB
# LimpiayCargaDatos
# TestServicioV1
# TestServicioV2
# LevantaServicios

# DEPENDENCIAS

#set_downstream()
#set_upstream()

PrepararEntorno.set_downstream([CapturaCodigoFuenteV1, CapturaCodigoFuenteV2, CapturaDatosA, CapturaDatosB])
DesempaquetaDatos.set_upstream([CapturaDatosA, CapturaDatosB])
DesempaquetaDatos.set_downstream(LimpiayCargaDatos)
LevantaDB.set_upstream([CapturaCodigoFuenteV1,CapturaCodigoFuenteV2])
LevantaDB.set_downstream(LimpiayCargaDatos)
TestServicioV1.set_upstream([LimpiayCargaDatos,CapturaCodigoFuenteV1])
CapturaCodigoFuenteV2.set_downstream(TestServicioV2)
LevantaServicios.set_upstream([TestServicioV1,TestServicioV2])