# Data Modeling for Tipico Project

## Introduction

This document provides an overview of the data model designed for the Tipico project. The data model is constructed to transform and organize data ingested from the Tipico API into a structured format suitable for analysis and reporting.

## Data Sources

The primary data source for this project is the Tipico API, which provides live event data. The data is fetched, processed, and stored in Amazon Redshift.

## Data Model Design

The data model focuses on the following key entities extracted from the Tipico API data:

1. **Events**
2. **Participants**
3. **Groups**
4. **Markets**
5. **Outcomes**

### Entities and Attributes

#### Events

- **Table**: `events`
- **Description**: Contains information about each event.
- **Columns**:
  - `event_id`: Unique identifier for the event.
  - `start_time`: Timestamp when the event is scheduled to start.
  - `message_time`: Timestamp when the event data was received.
  - `sport_type`: Type of sport for the event.
  - `match_state`: Current state of the match (e.g., ONGOING, COMPLETED).
  - `status`: Status of the event (e.g., RUNNING, ENDED).
  - `market_count`: Number of markets associated with the event.
  - `event_name`: Name of the event.
  - `last_modified_time`: Timestamp when the event data was last modified.

#### Participants

- **Table**: `participants`
- **Description**: Contains information about the participants in each event.
- **Columns**:
  - `participant_id`: Unique identifier for the participant.
  - `event_id`: Identifier for the associated event.
  - `name`: Name of the participant.
  - `position`: Position or role of the participant.
  - `abbreviation`: Abbreviation for the participant's name.

#### Groups

- **Table**: `groups`
- **Description**: Contains hierarchical information about the groups and subgroups associated with each event.
- **Columns**:
  - `group_id`: Unique identifier for the group.
  - `event_id`: Identifier for the associated event.
  - `group_name`: Name of the group.
  - `parent_group_id`: Identifier for the parent group (if applicable).
  - `parent_group_name`: Name of the parent group (if applicable).

#### Markets

- **Table**: `markets`
- **Description**: Contains information about the betting markets associated with each event.
- **Columns**:
  - `market_id`: Unique identifier for the market.
  - `event_id`: Identifier for the associated event.
  - `market_name`: Name of the market.
  - `market_type`: Type of the market (e.g., winner, score).
  - `parameters`: Parameters associated with the market.
  - `status`: Status of the market (e.g., OPEN, CLOSED).

#### Outcomes

- **Table**: `outcomes`
- **Description**: Contains information about the outcomes for each market.
- **Columns**:
  - `outcome_id`: Unique identifier for the outcome.
  - `market_id`: Identifier for the associated market.
  - `outcome_name`: Name of the outcome.
  - `is_traded`: Boolean indicating if the outcome is traded.
  - `format_decimal`: Decimal odds format.
  - `format_american`: American odds format.
  - `status`: Status of the outcome (e.g., ONGOING, SETTLED).
  - `true_odds`: True odds value.

## Data Relationships

The data model establishes relationships between different entities to ensure data integrity and enable complex queries. The key relationships are:

- `events` to `participants`: One-to-Many (an event can have multiple participants)
- `events` to `groups`: One-to-Many (an event can have multiple groups)
- `events` to `markets`: One-to-Many (an event can have multiple markets)
- `markets` to `outcomes`: One-to-Many (a market can have multiple outcomes)

## Data Transformations

Data is ingested from the Tipico API and stored in a raw format in Redshift. The dbt models then transform this raw data into structured tables based on the defined data model. The transformations include:

- Extracting nested JSON data and flattening it into relational tables.
- Type casting and data cleaning to ensure data consistency.
- Establishing relationships between tables through foreign keys.

## Example Queries

### Fetch All Events with Participants

```sql
SELECT
    e.event_id,
    e.event_name,
    e.start_time,
    p.participant_id,
    p.name AS participant_name
FROM
    events e
JOIN
    participants p ON e.event_id = p.event_id;
```
## Assumptions

The data is overridden each time the DAG runs; this is not an incremental load.
For the sake of ease, we have encoded all the variables in the code, but ideally, in a professional environment, we would be getting these through a secret management system.
For larger data volumes, we would use S3 and the S3 to Redshift operator. However, given the current data size, we are directly pushing data to Redshift over HTTPS.

## Conclusion
This data model provides a structured approach to organizing and analyzing Tipico event data. The use of Airflow for data ingestion and dbt for data transformation ensures a scalable and maintainable solution. The model is designed to be flexible, allowing for easy adjustments and additions as the project evolves.