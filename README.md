
## Prerequisites

1. **Docker**: Ensure you have Docker installed. Follow the installation instructions [here](https://docs.docker.com/get-docker/).
2. **Docker Compose**: Ensure you have Docker Compose installed. Follow the installation instructions [here](https://docs.docker.com/compose/install/).
3. **Airflow**: Included in the Docker setup.
4. **dbt**: Ensure you have dbt installed. Follow the installation instructions [here](https://docs.getdbt.com/dbt-cli/installation).
5. **Redshift Connection**: Ensure you have the necessary connection details (host, database, user, password, port) to connect to your Redshift instance.

## Setting Up the Project

### Airflow

1. **Clone the Repository**: 
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Build the Docker Image**:
    ```bash
    docker build . --tag extending_airflow:latest
    ```

3. **Start the Airflow Services**:
    Use Docker Compose to start the Airflow services.
    ```bash
    docker-compose up
    ```

4. **Configure Airflow Connections**:
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

### dbt

1. **Initialize the Project**:
    ```bash
    cd dbt
    dbt init tipico_project
    ```

2. **Configure the Profile**:
    Edit the `profiles.yml` file to include your Redshift connection details. This file is typically located at `~/.dbt/profiles.yml`. Example configuration:

    ```yaml
    tipico_project:
      target: dev
      outputs:
        dev:
          type: redshift
          host: <your-redshift-host>
          user: <your-redshift-username>
          password: <your-redshift-password>
          port: 5439
          dbname: <your-database-name>
          schema: core
          threads: 1
          keepalives_idle: 240
          connect_timeout: 10
          search_path: public
    ```

## Running the Project

### Airflow

1. **Deploy the DAG**:
    The `tipico_api_dag.py` file should already be in the `dags/` directory and automatically detected by Airflow.

2. **Trigger the DAG**:
    - Open the Airflow UI by navigating to `http://localhost:8080`.
    - Find the `tipico_api_dag` in the list of DAGs.
    - Toggle the DAG to "on" and trigger it manually if necessary.

### dbt

1. **Run dbt Models**:
    ```bash
    dbt run
    ```

    This command will execute all the models in the `models/` directory and create the corresponding tables in your Redshift instance.

2. **Testing**:
    ```bash
    dbt test
    ```

    This command will run the tests defined in the `schema.yml` file to validate your data.

3. **Generate Documentation**:
    ```bash
    dbt docs generate
    ```

    This command will generate documentation for your dbt project, including model descriptions and tests.

4. **Serve Documentation**:
    ```bash
    dbt docs serve
    ```

    This command will serve the documentation locally. You can access it in your browser at `http://localhost:8080`.

## Data Modeling

### Data Model Design

The data model focuses on the following entities from the Tipico API data:

- **Participants**
- **Group**
- **Markets** (including specifier and outcomes)
- **EventDetails**

### Assumptions

- The data is overridden each time the DAG runs; this is not an incremental load.
- For the sake of ease, we have encoded all the variables in the code, but ideally, in a professional environment, we would be getting these through a secret management system.
- For larger data volumes, we would use S3 and the S3 to Redshift operator. However, given the current data size, we are directly pushing data to Redshift over HTTPS.

### DBT Models

- **events.sql**: Model for events data.
- **participants.sql**: Model for participants data.
- **groups.sql**: Model for groups data.
- **markets.sql**: Model for markets data.
- **outcomes.sql**: Model for outcomes data.

## Troubleshooting

- **Connection Issues**: Ensure your Redshift cluster is running and that your connection details are correct in both Airflow and dbt settings.
- **Logs**: Check the logs for each task in the Airflow UI to diagnose issues.
- **dbt Commands**: Run `dbt debug` to check if your setup is correct and your connection to the database is working.

## Additional Resources

- [Airflow Documentation](https://airflow.apache.org/docs/)
- [Redshift Documentation](https://docs.aws.amazon.com/redshift/latest/dg/welcome.html)
- [dbt Documentation](https://docs.getdbt.com/docs/introduction)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

This `README.md` provides detailed steps for setting up, running, and troubleshooting your Airflow and dbt project. Make sure to replace placeholders like `<repository-url>` and `<your-redshift-host>` with your actual values.
