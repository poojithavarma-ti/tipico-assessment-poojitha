from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from airflow.utils.dates import days_ago
import requests
import json
import redshift_connector

# Define the DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'tipico_api_dag',
    default_args=default_args,
    description='DAG to call Tipico API and store data in Redshift',
    schedule_interval='*/10 * * * *',
)

# Define the function to call the API and save data to a local file
def retrieve_tipico_data_and_save_local(**kwargs):
    url = "https://trading-api.tipico.us/v1/pds/lbc/events/live?licenseId=US-NJ&lang=en&limit=18"
    response = requests.get(url)
    data = response.json()

    # Write data to a temporary file
    temp_file_path = '/tmp/tipico_data.json'
    with open(temp_file_path, 'w') as temp_file:
        json.dump(data, temp_file)
    
    # Push the file path to XCom
    kwargs['ti'].xcom_push(key='temp_file_path', value=temp_file_path)

# Define the function to create the table in Redshift
def create_table_in_redshift(**kwargs):

    host = '<your redshift host>'
    database = 'dev'
    user = 'admin'
    password = '<password>'
    port = 5439

    # Connect to Redshift using redshift_connector
    conn = redshift_connector.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=int(port)
    )
    cursor = conn.cursor()

    # Create table if not exists
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tipico_raw_data_updated (
        id BIGINT IDENTITY(1,1) PRIMARY KEY,
        raw_data SUPER,
        participants SUPER,
        group_info SUPER,
        markets SUPER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(create_table_query)
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

# Define the function to load data into Redshift
def load_data_to_redshift(**kwargs):
    # Retrieve the file path from XCom
    ti = kwargs['ti']
    temp_file_path = ti.xcom_pull(key='temp_file_path', task_ids='retrieve_tipico_data_and_save_local')

    host = '<your redshift host>'
    database = 'dev'
    user = 'admin'
    password = '<password>'
    port = 5439

    # Connect to Redshift using redshift_connector
    conn = redshift_connector.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=int(port)
    )
    cur = conn.cursor()

    with open(temp_file_path, 'r') as f:
        json_data = json.load(f)

    # Insert each JSON dictionary into the raw_data table
    insert_query = """
        INSERT INTO tipico_raw_data_updated (raw_data, participants, group_info, markets) VALUES (JSON_PARSE(%s), JSON_PARSE(%s), JSON_PARSE(%s), JSON_PARSE(%s))
    """

    print(json_data[0])
    for data in json_data:
        raw_data = json.dumps(data)
        participants = json.dumps(data.get('participants', []))
        group_info = json.dumps(data.get('group', {}))
        markets = json.dumps(data.get('markets', []))
        cur.execute(insert_query, (raw_data, participants, group_info, markets))

    # Commit the transaction
    conn.commit()

    # Close the connection
    cur.close()
    conn.close()

# Define the PythonOperator tasks
retrieve_data_task = PythonOperator(
    task_id='retrieve_tipico_data_and_save_local',
    python_callable=retrieve_tipico_data_and_save_local,
    provide_context=True,
    dag=dag,
)

create_table_task = PythonOperator(
    task_id='create_table_in_redshift',
    python_callable=create_table_in_redshift,
    provide_context=True,
    dag=dag,
)

load_data_task = PythonOperator(
    task_id='load_data_to_redshift',
    python_callable=load_data_to_redshift,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
retrieve_data_task >> create_table_task >> load_data_task
