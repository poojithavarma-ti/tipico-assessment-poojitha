# Tipico Data Modeling with dbt

## Introduction

This dbt project is designed to transform and model data retrieved from the Tipico API. The data is initially stored in Redshift in a raw format and then transformed into more structured tables using dbt.

## Project Structure

- `models/`: This directory contains the SQL files for the dbt models.
- `models/events.sql`: Model for events data.
- `models/participants.sql`: Model for participants data.
- `models/groups.sql`: Model for groups data.
- `models/markets.sql`: Model for markets data.
- `models/outcomes.sql`: Model for outcomes data.
- `schema.yml`: Contains tests and documentation for the models.
- `dbt_project.yml`: Configuration file for the dbt project.

## Prerequisites

1. **dbt Core**: Ensure you have dbt installed. Follow the installation instructions [here](https://docs.getdbt.com/dbt-cli/installation).
2. **Redshift Connection**: Ensure you have the necessary connection details (host, database, user, password, port) to connect to your Redshift instance.

## Setting Up the Project

1. **Clone the Repository**: 
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install dbt Redshift Adapter**: 
    ```bash
    pip install dbt-redshift
    ```

3. **Initialize the Project**:
    ```bash
    dbt init tipico_project
    ```

4. **Configure the Profile**:
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

## Detailed Model Descriptions

### Events Model

**File**: `models/events.sql`

Transforms raw event data into a structured table with the following columns:
- `event_id`: Unique identifier for each event.
- `start_time`: The start time of the event.
- `message_time`: The message time of the event.
- `sport_type`: The sport type of the event.
- `match_state`: The match state of the event.
- `status`: The status of the event.
- `market_count`: The number of markets in the event.
- `event_type`: The type of event.
- `updates_count`: The count of updates for the event.
- `event_name`: The name of the event.
- `last_modified_time`: The last modified time of the event.

### Participants Model

**File**: `models/participants.sql`

Transforms raw participant data into a structured table with the following columns:
- `participant_id`: Unique identifier for each participant.
- `event_id`: Foreign key referencing the events table.
- `name`: Name of the participant.
- `position`: Position of the participant.
- `abbreviation`: Abbreviation of the participant.

### Groups Model

**File**: `models/groups.sql`

Transforms raw group data into a structured table with the following columns:
- `group_id`: Unique identifier for each group.
- `event_id`: Foreign key referencing the events table.
- `name`: Name of the group.
- `parent_group_id`: Foreign key referencing the parent group.
- `parent_group_name`: Name of the parent group.
- `parent_parent_group_id`: Foreign key referencing the parent of the parent group.
- `parent_parent_group_name`: Name of the parent of the parent group.

### Markets Model

**File**: `models/markets.sql`

Transforms raw market data into a structured table with the following columns:
- `market_id`: Unique identifier for each market.
- `event_id`: Foreign key referencing the events table.
- `name`: Name of the market.
- `type`: Type of the market.
- `status`: Status of the market.
- `most_balanced_line`: Indicates if the market has the most balanced line.
- `sgp_eligible`: Indicates if the market is SGP eligible.

### Outcomes Model

**File**: `models/outcomes.sql`

Transforms raw outcome data into a structured table with the following columns:
- `outcome_id`: Unique identifier for each outcome.
- `market_id`: Foreign key referencing the markets table.
- `name`: Name of the outcome.
- `is_traded`: Indicates if the outcome is traded.
- `format_decimal`: Decimal format of the outcome.
- `format_american`: American format of the outcome.
- `status`: Status of the outcome.
- `true_odds`: True odds of the outcome.

## Additional Resources

- [dbt Documentation](https://docs.getdbt.com/docs/introduction)
- [Redshift Documentation](https://docs.aws.amazon.com/redshift/latest/dg/welcome.html)

## Troubleshooting

- **Connection Issues**: Ensure your Redshift cluster is running and that your connection details in `profiles.yml` are correct.
- **dbt Commands**: Run `dbt debug` to check if your setup is correct and your connection to the database is working.
- **Logs**: Check the logs in the `logs/` directory for detailed error messages.

---

This `README.md` provides detailed steps for setting up, running, and documenting your dbt project. It also includes descriptions of the models and their columns. Make sure to replace placeholders like `<repository-url>` and `<your-redshift-host>` with your actual values.
