# Tipico Data Ingestion with Airflow

## Introduction

This repository contains an Airflow DAG designed to automate the ingestion of data from the Tipico API and store it in an Amazon Redshift database. The data is fetched, processed, and stored in a raw format, ready for further transformations and analysis.

## Project Structure

- `dags/`: This directory contains the Airflow DAG scripts.
  - `tipico_api_dag.py`: The main DAG script to call the Tipico API and store the data in Redshift.
- `docker-compose.yml`: Docker Compose configuration file.
- `Dockerfile`: Dockerfile to build the custom Airflow image.

## Prerequisites

1. **Docker**: Ensure you have Docker installed. Follow the installation instructions [here](https://docs.docker.com/get-docker/).
2. **Docker Compose**: Ensure you have Docker Compose installed. Follow the installation instructions [here](https://docs.docker.com/compose/install/).
3. **Redshift Connection**: Ensure you have the necessary connection details (host, database, user, password, port) to connect to your Redshift instance.

## Setting Up the Project

1. **Clone the Repository**: 
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Build the Docker Image**:
    ```bash
    docker build . --tag extending_airflow:latest
    ```

3. **Configure Airflow Connections**:
    - **Redshift Connection**:
      1. Navigate to the Airflow UI once the services are up.
      2. Go to Admin -> Connections.
      3. Create a new connection:
         - **Conn Id**: `redshift_conn_id`
         - **Conn Type**: `Postgres`
         - **Host**: `<your-redshift-host>`
         - **Schema**: `<your-database-name>`
         - **Login**: `<your-username>`
         - **Password**: `<your-password>`
         - **Port**: `5439`

## Running the Project

1. **Start the Airflow Services**:
    Use Docker Compose to start the Airflow services.
    ```bash
    docker-compose up
    ```

2. **Access the Airflow UI**:
    Open your web browser and navigate to `http://localhost:8080`. You should see the Airflow UI.

3. **Deploy the DAG**:
    The `tipico_api_dag.py` file should already be in the `dags/` directory and automatically detected by Airflow.

4. **Trigger the DAG**:
    - In the Airflow UI, find the `tipico_api_dag` in the list of DAGs.
    - Toggle the DAG to "on" and trigger it manually if necessary.

## Airflow DAG Details

### `tipico_api_dag.py`

This DAG retrieves data from the Tipico API, processes it, and stores it in Redshift.

#### DAG Configuration

- **DAG Name**: `tipico_api_dag`
- **Schedule Interval**: Every 10 minutes (`*/10 * * * *`)
- **Tasks**:
  1. **Retrieve Data Task**: Calls the Tipico API and saves the data to a local file.
  2. **Create Table Task**: Creates the necessary table in Redshift if it doesn't already exist.
  3. **Load Data Task**: Loads the data from the local file into the Redshift table.

## Troubleshooting

- **Connection Issues**: Ensure your Redshift cluster is running and that your connection details are correct in the Airflow connection settings.
- **Logs**: Check the logs for each task in the Airflow UI to diagnose issues.

## Additional Resources

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Redshift Documentation](https://docs.aws.amazon.com/redshift/latest/dg/welcome.html)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

This `README.md` provides detailed steps for setting up, running, and troubleshooting your Airflow DAG using Docker Compose. Make sure to replace placeholders like `<repository-url>` and `<your-redshift-host>` with your actual values.
