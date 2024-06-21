{{ config(
    materialized='table',
    schema='core'
) }}

with raw_events as (
    select
        cast(json_extract_path_text(json_serialize(raw_data), 'startTime') as timestamp) as start_time,
        cast(json_extract_path_text(json_serialize(raw_data), 'messageTime') as timestamp) as message_time,
        json_extract_path_text(json_serialize(raw_data), 'sportType') as sport_type,
        json_extract_path_text(json_serialize(raw_data), 'matchState') as match_state,
        json_extract_path_text(json_serialize(raw_data), 'status') as status,
        cast(json_extract_path_text(json_serialize(raw_data), 'marketCount') as int) as market_count,
        json_extract_path_text(json_serialize(raw_data), 'eventType') as event_type,
        cast(json_extract_path_text(json_serialize(raw_data), 'updatesCount') as int) as updates_count,
        json_extract_path_text(json_serialize(raw_data), 'eventName') as event_name,
        cast(json_extract_path_text(json_serialize(raw_data), 'lastModifiedTime') as timestamp) as last_modified_time
    from
        {{ ref('tipico_raw_data') }}
)

select * from raw_events
